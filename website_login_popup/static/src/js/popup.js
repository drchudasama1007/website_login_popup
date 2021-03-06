odoo.define('website_login_popup.popup', function(require) {
    'use strict';

    var sAnimations = require('website.content.snippets.animation');
    var publicWidget = require('web.public.widget');
    var Widget = require('web.Widget');
    var core = require('web.core');
    var _t = core._t
    var ajax = require('web.ajax');
    var config = require('web.config');
//    var sale = new sAnimations.registry.WebsiteSale();

    sAnimations.registry.reset_password_popup = sAnimations.Class.extend({
        selector: "#wrapwrap",
        start: function () {
            console.log("start function=========================")
            self = this;
            self.customerLogin();
            self.customerRegistration();
        },

        resetPassword: function(){
            $("#loginRegisterPopup .oe_reset_password_form").submit(function(e) {
                var $form = $('#loginRegisterPopup .oe_reset_password_form');
                e.preventDefault();
                var url = '/web/reset_password?'+$form.serialize();
                    $.ajax({
                    url: url,
                    type: 'POST',
                    success: function(data) {
                        var oe_reset_password_form_error = $(data).find('.te_reset_password_form').find('.alert.alert-danger').html();
                        var oe_reset_password_form_success  = $(data).find('main .oe_website_login_container').find('.alert.alert-success').html();
                        if($(data).find('.te_reset_password_form').find('.alert.alert-danger').length) {
                            $("#loginRegisterPopup .oe_reset_password_form .te_error-success").replaceWith("<div class='te_error-success alert alert-danger mt16 mb16 mx-3'>" + oe_reset_password_form_error + "</div>");
                        }
                        if($(data).find('main .oe_website_login_container').find('.alert.alert-success').length) {
                            $("#loginRegisterPopup .oe_reset_password_form .te_error-success").replaceWith("<div class='te_error-success alert alert-success mt16 mb16 mx-3'>" + oe_reset_password_form_success + "</div>");
                        }
                    },
                });
            });
        },

        customerLogin: function(){
            $(".login_signup_form").submit(function(e) {

                var $form = $('.login_signup_form');
                e.preventDefault();
                var email = $form.find('#login').val();
                var pass = $form.find('#password').val();
                console.log("Form Submit Thyu===============",email,pass)
                ajax.jsonRpc('/web/login_custom', 'call', {'login':email,'password':pass}).then(function(data) {
                    if(!data.login_success){
                        $(".login_signup_form .te_error-success").replaceWith("<div class='te_error-success alert alert-danger mt16 mb16 mx-3 text-left'>" + data.error + "</div>");
                    }
                    else{
                        if (data.user_type == 'internal') {
                            $(location).attr('href', '/web');
                        } else {
                            $(location).attr('href', '/my');
                        }
                    }
                });
            });
        },

        customerRegistration: function(){
            $(".register_signup_form").submit(function(e) {
                console.log("register_signup_form===================")
                var $form = $('.register_signup_form');
                e.preventDefault();
                var email = $form.find('#login').val();
                var name = $form.find('#name').val();
                var password = $form.find('#password').val();
                var confirm_password = $form.find('#confirm_password').val();
                console.log("register_signup_form======value=============",email,name,password,confirm_password)
                ajax.jsonRpc('/web/signup_custom', 'call', {'login':email,'name':name,'password':password,'confirm_password':confirm_password,'redirect':'','token':''}).then(function(data) {


                    if(!data.is_success){
                        $(".register_signup_form .te_error-success").replaceWith("<div class='te_error-success alert alert-danger mt16 mb16 mx-3 text-left'>" + data.error + "</div>");
                    } else {
                        $(location).attr('href', '/my');
                    }
                });
            });
        },

    });

    $(document).ready(function() {

        $(document).on('click', '.login', function(){
            $('#login_form').show();
            $('#signup_form').hide();
            $('.login').css('border-bottom', '1px solid black');
            $('.signup').css('border-bottom', '1px solid white');
        });

        $(document).on('click', '.signup', function(){
            $('#login_form').hide();
            $('#signup_form').show();
            $('.signup').css('border-bottom', '1px solid black');
            $('.login').css('border-bottom', '1px solid white');
        });

    })

})