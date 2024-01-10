#!/bin/bash
dropdb blogly-3
createdb blogly-3
psql blogly-3 < blogly-3.sql
