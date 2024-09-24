#!/bin/bash

rm -f stock_digest.tar

docker build -t stock_digest .

docker save stock_digest -o stock_digest.tar