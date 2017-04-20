
#!/bin/bash

# Take site list from command line argument

if [[ $1 -eq 0 ]]
    then
    	echo
    	echo "NAME:"
    	echo "	random_dns_lookup.sh"
    	echo
            echo "USAGE:"
            echo "	./random_dns_lookup.sh <list-of-sites> <max-time> <query-multiplier>"
    	echo
    	echo "DESCRIPTION:"
    	echo "	<list-of-sites>		A text file containing urls"
    	echo "	<max-time>		A maximum amount of seconds to be waited between queries."
      echo "        <query-multiplier>      How many times one query will be repeated."
    	echo
    	echo "EXAMPLE:"
    	echo
    	echo "	./random_dns_lookup.sh goodsites.txt 300 20"
    	echo
    	echo "	A random site from goodsites.txt will be used to make 20 dns queries every 1-300 seconds."
    	echo
      exit
    else
	     echo "Continuing..."
fi

list=$1
echo "Using: " $list

# Take timeout from command line argument
if [[ $2 -eq 0 ]]
  then
    time_out=100
  else
    time_out=$2
fi

# Take multiplier from command line argument
if [[ $3 -eq 0 ]]
  then
    multiplier=1
  else
    multiplier=$3
fi

# Make nslookups until the end of the world as we know it
while true
  do

    # Take random site
    site=`shuf -n 1 $list`

    echo
    echo $site
    echo

    # Make nslookup using above random site and user provided  multiplier
    for (( i = 0; i <= multiplier; i++ ));
      do
        nslookup $site
    done

    echo "-----------------------------------------"

    # Sleep for random amount of seconds between 1 and input from the user
    sleep $(shuf -i1-$time_out -n1)

done
