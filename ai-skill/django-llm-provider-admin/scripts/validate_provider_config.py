import json
import sys

def validate(config):
    errors = []

    required = ["provider_type", "model_name", "is_active"]
    for field in required:
        if field not in config:
            errors.append(f"missing required field: {field}")

    if "timeout_seconds" in config and config["timeout_seconds"] <= 0:
        errors.append("timeout_seconds must be greater than 0")

    if "priority" in config and config["priority"] < 0:
        errors.append("priority must be non-negative")

    return errors

def main():
    if len(sys.argv) < 2:
        print("usage: python validate_provider_config.py '{\"provider_type\": \"openai\"}'")
        sys.exit(1)

    config = json.loads(sys.argv[1])
    errors = validate(config)

    if errors:
        print(json.dumps({"valid": False, "errors": errors}, indent=2))
    else:
        print(json.dumps({"valid": True, "errors": []}, indent=2))

if __name__ == "__main__":
    main()