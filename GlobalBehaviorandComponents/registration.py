import os
import base64
import json
import requests
import logging

#import functions
from functools import wraps
from flask import render_template, url_for, redirect, session,request
from flask import send_from_directory, make_response
from flask import Blueprint,g
from flask import Flask, current_app as app
from utils.okta import OktaAuth, OktaAdmin, TokenUtil
from utils.udp import SESSION_INSTANCE_SETTINGS_KEY, get_app_vertical

from GlobalBehaviorandComponents.validation import is_authenticated, get_userinfo

logger = logging.getLogger(__name__)

#set blueprint
gbac_registration_bp = Blueprint('gbac_registration_bp', __name__,template_folder='templates', static_folder='static', static_url_path='static')

#Required for Registration Page
@gbac_registration_bp.route("/registration")
def registration_bp():
    logger.debug("Registration")
    return render_template("/registration.html", templatename=get_app_vertical(), config=session[SESSION_INSTANCE_SETTINGS_KEY])


@gbac_registration_bp.route("/completeregistration", methods=["POST"])
def completeregistration_bp():
    logger.debug("Complete Registration")
    user_data = {
                "profile": {
                    "firstName": request.form.get('firstname'),
                    "lastName": request.form.get('lastname'),
                    "email": request.form.get('email'),
                    "login": request.form.get('email'),
                    "organization": request.form.get('organization')
                }
            }
    logger.debug(user_data)
    okta_admin = OktaAdmin(session[SESSION_INSTANCE_SETTINGS_KEY])
    test = okta_admin.create_user(user=user_data,activate_user='true')
    logger.debug(test)
    message = "Registration Complete! Please check your email."
    return redirect(url_for("gbac_bp.gbac_login", _external="True", _scheme="https",message=message))