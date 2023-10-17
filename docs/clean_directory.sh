#!/bin/bash

# Delete all files and folders in the directory: /pythainlp/docs/<version>

# $1 : FTP_USER
# $2 : FTP_PASSWORD
# $3 : FTP_HOST
# $4 : Branch name

FTP_USER=$1
FTP_PASSWORD=$2
FTP_HOST=$3
BRANCH_NAME=$4

remove_all_files()
{
    # DIRECTORY=$1
    echo "Delete files in: $1"
    for f in `curl --list-only --ftp-create-dirs --ipv4 ftp://$FTP_USER:$FTP_PASSWORD@$FTP_HOST/$1/`; do
        if [[ -d "$f" ]] || [[ "$f" = _* ]] || [[ "$f" = .doctree ]] || [[ "$f" != *"."* ]]; then
            echo "--- deleting files in folder: $1/$f";
            remove_all_files $1/$f
        else
            echo "Delete a file: $f"
            curl --ipv4 ftp://$FTP_USER:$FTP_PASSWORD@$FTP_HOST -Q "DELE $1/$f"
        fi
    done
}

remove_empty_folders()
{

  echo "Delete empty folders in: $1"
    for f in `curl --list-only --ftp-create-dirs --ipv4 ftp://$FTP_USER:$FTP_PASSWORD@$FTP_HOST/$1/`; do
        if [[ -d "$f" ]] || [[ "$f" = _* ]] || [[ "$f" = fonts ]] || [[ "$f" = pythainlp ]] || [[ "$f" = .doctree ]] || [[ "$f" != *"."* ]]; then
            echo "--- Deleting folders in: $1/$f";
            remove_empty_folders $1/$f
            curl --ipv4 ftp://$FTP_USER:$FTP_PASSWORD@$FTP_HOST -Q "RMD $1/$f"
        else
            echo "Delete a folder: $f"
            curl --ipv4 ftp://$FTP_USER:$FTP_PASSWORD@$FTP_HOST -Q "RMD $1/$f"
        fi
    done
}

echo "Start removing all files within: public_html/pythainlp/docs/$BRANCH_NAME/";

remove_all_files public_html/pythainlp/docs/$BRANCH_NAME;

echo "Start removing all empty folders within: public_html/pythainlp/docs/$BRANCH_NAME/";

remove_empty_folders public_html/pythainlp/docs/$BRANCH_NAME;

echo "Done.";
