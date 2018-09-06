if [ -f "flaskr.db" ]; then
   echo "Database exists."
else
   echo "Database does not exist."
   echo "Proceeding to create database."
   eval $(python3 db.py)
fi

if command -v python3 &>/dev/null; then
    echo Python 3 is installed
else
    echo Python 3 is not installed
fi

export FLASK_APP=flaskr
eval $(flask run)
