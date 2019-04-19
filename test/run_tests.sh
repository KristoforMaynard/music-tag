#!/usr/bin/env bash
#

other_args=""
stop_on_err=0
tests="?"

print_usage() {
cat << EOF
Usage: ${0##*/} [-h] [-t test1[,test2[,...]]] [-a "ARGS"]

Run all tests

  Optional Arguments:
    -h          help
    -S          Stop on first error
    -t TESTS    comma separated list of explicit tests to run, note
                that you should not include the _test part of the name,
                i.e., use mvi instead of test_mvi
    -a ARGS     misc. arguments to pass to all test scripts

EOF
exit $1
}

OPTIND=1
while getopts "h?Sa:t:" arg; do
  case $arg in
    h|\?)
      print_usage 0;;
    a) other_args="${OPTARG}";;
    S) stop_on_err=1;;
    t) tests="${OPTARG}";;
    *) print_usage 1;;
  esac
done
shift $((OPTIND-1))

function abspath() {
    # generate absolute path from relative path
    # $1     : relative filename
    # return : absolute path
    if [ -d "$1" ]; then
        # dir
        (cd "$1"; pwd)
    elif [ -f "$1" ]; then
        # file
        if [[ $1 == */* ]]; then
            echo "$(cd "${1%/*}"; pwd)/${1##*/}"
        else
            echo "$(pwd)/$1"
        fi
    fi
}


GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'
TOTALC=${NC}
PASSC=${GREEN}
XFAILC=${CYAN}
FAILC=${RED}

sdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

tests0="${tests//,/ }"
tests=""
for t in ${tests0}; do
  tests="${tests} $(ls ${sdir}/test_*${t}* | grep -Ev '.(log|stderr|stdout)$')"
done

total=0
passed=0
xfailed=0
failed=0

for test in ${tests}; do
  test="$(abspath "${test}")"

  if [[ $test == *.py ]]; then
    cmd="/usr/bin/env python ${test} ${other_args}"
  elif [[ $test == *.sh ]]; then
    cmd="/usr/bin/env bash ${test} ${other_args}"
  elif [[ -x ${test} ]]; then
    cmd="./${test} ${other_args}"
  else
    echo "!! Don't know how to run:" >&2
    echo "!! ${test}" >&2
    echo "!! Try giving it execute permission" >&2
    cmd="false"
  fi

  fstdout="${test}.stdout"
  fstderr="${test}.stderr"
  flog="${test}.log"

  # ${cmd} > >(tee ${fstdout}) 2> >(tee ${fstderr} >&2)
  status="$(cd ${sdir} && ${cmd} 1>${fstdout} 2>${fstderr}; echo "$?")"
  ! cat ${fstderr} | grep -qE "^XFAIL:"
  xfail_status=$?

  echo "===== STDOUT =====" > ${flog}
  cat ${fstdout} >> ${flog}
  echo "===== STDERR =====" >> ${flog}
  cat ${fstderr} >> ${flog}

  total=$((total+1))
  if [ ${status} -eq 0 ]; then
    passed=$((passed+1))
    echo -e "${PASSC}PASS${NC}: $(basename ${test})"
    rm ${flog}
  elif [ ${xfail_status} -ne 0 ]; then
    xfailed=$((xfailed+1))
    echo -e "${XFAILC}XFAIL${NC}: $(basename ${test})"
    cat ${fstderr}
  else
    failed=$((failed+1))
    echo -e "${FAILC}FAIL${NC}: $(basename ${test})"
    cat ${fstderr}
  fi

  rm ${fstdout} ${fstderr}

  if [[ ${stop_on_err} -ne 0 && ${status} -ne 0 && ${xfail_status} -eq 0 ]]; then
    exit 1
  fi

done

echo -e "${RED}=====================${NC}"
echo -e "${TOTALC}TOTAL: ${total}${NC}"
echo -e "${PASSC}PASS:  ${passed}${NC}"
echo -e "${XFAILC}XFAIL: ${xfailed}${NC}"
echo -e "${FAILC}FAIL:  ${failed}${NC}"
echo -e "${RED}=====================${NC}"

#############################################
# exit with the status from the actual tests
exit ${failed}

##
## EOF
##
