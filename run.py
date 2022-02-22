from flask import Flask, jsonify, request, abort, render_template
import json
from app.views import create_app

app=create_app()


if __name__=='__main__':
    app.run(debug=True)
    