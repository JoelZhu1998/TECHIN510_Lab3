import os
from dataclasses import dataclass

import streamlit as st
import psycopg2
from dotenv import load_dotenv

load_dotenv()

con = psycopg2.connect(os.getenv("postgres://postgres.uyhwdtfzmilxpyqfoyfb:QBYS54wsn!!!@aws-0-us-west-1.pooler.supabase.com:5432/postgres"))
cur = con.cursor()
