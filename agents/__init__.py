import importlib

# Import subpackage with hyphen in name
psycological_analyser = importlib.import_module(".psycological-analyser", package="agents")

# Export the functions
analyse_woman_psicological_issue = psycological_analyser.analyse_woman_psicological_issue

__all__ = ["analyse_woman_psicological_issue"]
