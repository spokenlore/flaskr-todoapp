if [ -f "flaskr.db" ]; then
   echo "Database exists."
else
   echo "Database does not exist."
   echo "Proceeding to create database."
   eval $(python3 db.py)
fi

export FLASK_APP=flaskr
eval $(flask run)
