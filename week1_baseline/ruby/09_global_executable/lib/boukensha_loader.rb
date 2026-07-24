# BoukenshaLoader resolves which step folder to load from, then boots the REPL.
#
# Resolution order:
#   1. BOUKENSHA_PATH environment variable (selects which *step* lib to load)
#   2. ~/.boukensharc  (YAML with boukensha_path, or legacy single path)
#   3. The lib/ directory bundled inside this gem (step 8 — the latest release)
#
# Config directory (settings.yaml, .env, system.md) is separate:
#   1. BOUKENSHA_DIR environment variable
#   2. ~/.boukensharc boukensha_dir key
#   3. ~/.boukensha default
#
# Examples:
#   boukensha                                                              # uses bundled lib + ~/.boukensha
#   BOUKENSHA_PATH=~/Sites/boukensha/04_api_client boukensha              # loads step 4
#   BOUKENSHA_DIR=~/projects/mybot/.boukensha boukensha                   # custom config dir
#   echo "boukensha_path: ~/Sites/boukensha/08_the_repl_loop" > ~/.boukensharc
require "yaml"

module BoukenshaLoader
  # Absolute path to this gem's own bundled boukensha lib.
  BUNDLED_LIB = File.expand_path("../boukensha.rb", __FILE__)
  RC_FILE = File.expand_path("~/.boukensharc").freeze

  def self.resolve
    rc = rc_config

    # 1. Env var wins.
    if ENV["BOUKENSHA_PATH"]
      dir  = File.expand_path(ENV["BOUKENSHA_PATH"])
      main = File.join(dir, "lib", "boukensha.rb")
      return main if File.exist?(main)

      abort <<~MSG
        boukensha: BOUKENSHA_PATH is set but no lib/boukensha.rb found at:
               #{dir}
               Make sure BOUKENSHA_PATH points to a step folder, e.g.:
               BOUKENSHA_PATH=~/Sites/boukensha/07_the_repl_loop boukensha
      MSG
    end

    # 2. ~/.boukensharc
    dir = rc["boukensha_path"]
    unless dir.to_s.empty?
      main = File.join(File.expand_path(dir), "lib", "boukensha.rb")
      return main if File.exist?(main)

      abort <<~MSG
        boukensha: ~/.boukensharc points to #{dir}
               but no lib/boukensha.rb was found there.
               Update ~/.boukensharc or remove it to use the bundled default.
      MSG
    end

    # 3. Bundled default.
    BUNDLED_LIB
  end

  def self.load_and_start_repl
    configure_env_from_rc

    main = resolve
    step_dir = File.dirname(File.dirname(main))

    puts "[boukensha] loading from: #{step_dir}" if ENV["BOUKENSHA_DEBUG"]

    require main

    unless Boukensha.respond_to?(:repl)
      abort <<~MSG
        boukensha: the step at #{step_dir}
               does not support the interactive REPL (added in step 7).
               Run its examples directly, e.g.:
                 ruby #{step_dir}/examples/*.rb
               Or point BOUKENSHA_PATH at step 7 or later.
      MSG
    end

    Boukensha.repl
  end

  def self.configure_env_from_rc
    dir = rc_config["boukensha_dir"]
    ENV["BOUKENSHA_DIR"] ||= File.expand_path(dir) unless dir.to_s.empty?
  end

  def self.rc_config
    return {} unless File.exist?(RC_FILE)

    raw = File.read(RC_FILE).strip
    return {} if raw.empty?

    parsed = YAML.safe_load(raw, permitted_classes: [], aliases: false)
    case parsed
    when Hash
      parsed.transform_keys(&:to_s)
    when String
      { "boukensha_path" => parsed }
    else
      { "boukensha_path" => raw }
    end
  rescue Psych::SyntaxError
    { "boukensha_path" => raw }
  end
end
