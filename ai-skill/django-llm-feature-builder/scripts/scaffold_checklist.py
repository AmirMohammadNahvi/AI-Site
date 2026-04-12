from dataclasses import dataclass, asdict
import json
import sys

@dataclass
class FeatureChecklist:
    feature_name: str
    needs_model: bool = False
    needs_admin: bool = False
    needs_serializer: bool = True
    needs_view: bool = True
    needs_service: bool = True
    needs_task: bool = False
    needs_logging: bool = True
    needs_tests: bool = True

def main():
    feature_name = sys.argv[1] if len(sys.argv) > 1 else "new_feature"
    checklist = FeatureChecklist(feature_name=feature_name)
    print(json.dumps(asdict(checklist), indent=2))

if __name__ == "__main__":
    main()