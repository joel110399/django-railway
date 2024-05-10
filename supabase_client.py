
from supabase import create_client


def get_supabase_client():
    url = "https://wldrwmnodywsdsdzuuwu.supabase.co"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndsZHJ3bW5vZHl3c2RzZHp1dXd1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTQ3ODk4NjYsImV4cCI6MjAxMDM2NTg2Nn0.JbZw-AXnpJ8NPBgkAB4mLkpA8SxerKIdMCmZEwDnbow"

    return create_client(url, key)
