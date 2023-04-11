#!/bin/bash

installed=$(which psql)
if [[ -z "$installed" ]]; then
    echo "Postgres not detected."
    echo "Start collecting Postgres..."
    brew=$(which brew)
    if [[ -z "$brew" ]]; then
        echo "homebrew not installed."
        echo "Start collecting brew..."
        $(/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)")

        # exporting path
        NEW_PATH="/opt/homebrew/bin"

        # Check if the directory is already in the PATH
        (echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"') >> /Users/jeffy/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
        brew update
        # installing postgresql
        brew install postgresql@14
    else
        echo "installing Postgresql."
        brew install postgresql@14
    fi
else
    echo "prerequisites satisfied."
fi

echo "Start services..."
brew services start postgresql@14
sleep 5
echo "Start building schema..."
psql -d postgres -f ./schema.sql
echo "Building success!"
brew services stop postgresql@14