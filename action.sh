#!/usr/bin/env bash
# Composite-action entry point: generate a combined third-party license CSV from a
# distribution ZIP (--zippaths) or a built Maven project (--project). Inputs come from
# the INPUT_* env vars set in action.yml.

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
creator="${script_dir}/thirdPartyLicenseCSVCreator.py"

distribution_zip="${INPUT_DISTRIBUTION_ZIP:-}"
project_path="${INPUT_PROJECT_PATH:-}"
version="${INPUT_VERSION:-}"
output_dir="${INPUT_OUTPUT_DIR:-deploy_dir}"
project_name="${INPUT_PROJECT_NAME:-}"

fail() {
  echo "::error::$*"
  exit 1
}

# Validate inputs (exactly one source, version required).
[ -n "${version}" ] || fail "The 'version' input is required."
if [ -n "${distribution_zip}" ] && [ -n "${project_path}" ]; then
  fail "Provide only one of 'distribution-zip' or 'project-path', not both."
fi
if [ -z "${distribution_zip}" ] && [ -z "${project_path}" ]; then
  fail "One of 'distribution-zip' or 'project-path' must be provided."
fi
command -v python3 >/dev/null 2>&1 || fail "python3 is required but was not found on PATH."

mkdir -p "${output_dir}"

# This action always produces a single combined CSV (one csv_path output).
args=(--version "${version}" --output "${output_dir}" --combined)
[ -n "${project_name}" ] && args+=(--name "${project_name}")

tmp=""
cleanup() { [ -n "${tmp}" ] && rm -rf "${tmp}" || true; }
trap cleanup EXIT

if [ -n "${distribution_zip}" ]; then
  # ZIP mode: unzip, then collect every jar for --zippaths.
  command -v unzip >/dev/null 2>&1 || fail "unzip is required for ZIP mode but was not found on PATH."

  # Resolve the glob explicitly (no `ls` parsing) and require exactly one match.
  shopt -s nullglob
  matches=( ${distribution_zip} )
  shopt -u nullglob
  if [ "${#matches[@]}" -eq 0 ]; then
    fail "No distribution ZIP matched '${distribution_zip}'."
  elif [ "${#matches[@]}" -gt 1 ]; then
    fail "Multiple distribution ZIPs matched '${distribution_zip}': ${matches[*]}"
  fi
  zip="${matches[0]}"
  [ -f "${zip}" ] || fail "Distribution ZIP not found: '${zip}'."

  tmp="$(mktemp -d)"
  unzip -q "${zip}" -d "${tmp}"

  zippaths=""
  while IFS= read -r -d '' file; do
    zippaths+="${file}|"
  done < <(find "${tmp}" -name "*.jar" -print0)
  zippaths="${zippaths%|}"
  [ -n "${zippaths}" ] || fail "No .jar files were found inside the distribution ZIP '${zip}'."

  args+=(--zippaths "${zippaths}")
else
  # Project mode: scan a built checkout for THIRD-PARTY.txt files.
  [ -d "${project_path}" ] || fail "The 'project-path' directory does not exist: '${project_path}'."
  args+=(--project "${project_path}")
fi

# Run the creator and capture its output; it prints "Created <path>" per CSV.
gen_output="$(python3 "${creator}" "${args[@]}")"
echo "${gen_output}"

# Export the generated CSV path (combined mode prints a single "Created <path>" line).
csv=""
while IFS= read -r line; do
  case "${line}" in
    "Created "*) csv="${line#Created }"; break ;;
  esac
done <<< "${gen_output}"
[ -n "${csv}" ] || fail "No CSV file was produced in '${output_dir}'."
echo "csv_path=${csv}" >> "${GITHUB_OUTPUT}"

