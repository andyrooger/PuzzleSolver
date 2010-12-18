#!/bin/sh

cd `dirname $0`
cd solver

java Solve `cd ../conf; pwd`
