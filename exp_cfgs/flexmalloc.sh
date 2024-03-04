#!/bin/bash


library=libflexmalloc
if [[ ${FLEXMALLOC_DEBUG} == "1" ]] || [[ ${FLEXMALLOC_DEBUG} == "enabled" ]] || [[ ${FLEXMALLOC_DEBUG} == "yes" ]] ; then
		library=${library}_dbg
fi

if [[ $# -lt 3 ]] ; then
	echo Error! Check for parameters!
	echo 1st parameter: memory definitions
	echo 2nd parameter: data-object allocation locations
	echo 3rd and successive parameters: application process
	exit
fi

if [[ ! -f ${1} ]] ; then
	echo Warning! Cannot locate given definitions file ${1}
fi

if [[ ! -f ${2} ]] ; then
	echo Warning! Cannot locate given locations file ${2}
fi

export FLEXMALLOC_DEFINITIONS=${1}
export FLEXMALLOC_LOCATIONS=${2}

# # If MPI rank is 0 or non MPI-execution, set minimum verbosity
if [[ "${PMI_RANK}" == "0" || "${PMI_RANK}" == "" ]] ; then
	# Set verbose level 1 if no verbosity requested in rank 0
	if [[ "${FLEXMALLOC_VERBOSE}" == "" ]] ; then
		export FLEXMALLOC_VERBOSE=1
	fi
	#LD_PRELOAD=${FLEXMALLOC_HOME}/lib/${library}.so ${@:3}
	#gdb -ex "set startup-with-shell off" -ex "set env LD_PRELOAD ${FLEXMALLOC_HOME}/lib/${library}.so" -ex r --args ${@:3}
	gdb -ex "set startup-with-shell off" -ex "set env LD_PRELOAD ${FLEXMALLOC_HOME}/lib/${library}.so" --args ${@:3}

	#LD_PRELOAD=${FLEXMALLOC_HOME}/lib/${library}.so ${@:3} &
	#pid=$!
	#perf record --pid=$pid -g -F 99
	#wait $pid

else 
	export FLEXMALLOC_DEBUG=no
	export FLEXMALLOC_VERBOSE=0
	LD_PRELOAD=${FLEXMALLOC_HOME}/lib/${library}.so ${@:3} > /dev/null 2> /dev/null
fi

