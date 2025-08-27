#!/usr/bin/env python
# src/project/main.py
import sys
from crew import incidentHandling
import streamlit as st


def run():
    """
    Run the crew.
    """
    inputs = {
        'input': 'Hello, I have a problem with my computer. This is terrible.'
    }

    crew_instance = incidentHandling().crew()
    result = crew_instance.kickoff(inputs=inputs)

    print("\n\n=== Finish ===\n\n")
    print(result)

if __name__ == '__main__':
    run()