#!/bin/bash
nc radarcape.local 30003 | python3 record.py --token $(cat token.txt)
