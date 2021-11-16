import React from 'react';
import {
    Redirect
} from "react-router-dom";
import {login} from "./App";


function SignUp(props) {
    return (
      <div className="subscribe content">
        <h1>Sign Up</h1>
        <h3>Enter an email and a phone number (text, optional), and a password to sign up for 3STAT</h3>
        <SubscribeForm logged_in={props.logged_in} update_login={props.update_login}  />
      </div>
    );
  }

  class SubscribeForm extends React.Component {
    constructor(props) {
      super(props);
      console.log("Subscribe")
      console.log(props);
      this.state = {
        email: '',
        phone: '',
        password: ''
      }
  
      this.handleChange = this.handleChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
    }
  
    handleChange(event) {
      const name = event.target.name;

      this.setState({[name]: event.target.value});
    }
  
    handleSubmit(event) {
      // alert('Email submitted: ' + this.state.email + ' / Phone # submitted: ' + this.state.phone);
      event.preventDefault();
      let account = {
          'email' : this.state.email,
          'phone' : this.state.phone,
          'password' : this.state.password
      }
      if (event.nativeEvent.submitter.value === "Sign Up"){
      fetch('/api/authentication/register/', {
          method: 'post',
          body: JSON.stringify(account),
          headers: {
              'Content-Type': 'application/json'
          }
      }).then(response => response.json())
        .then(token => {
          if (token.result.access_token){
              login(token);
              this.props.update_login(true);
          }
          else {
           alert('Bad Username or Password, or Already Registered');
          }
        })
      }
      else if (event.nativeEvent.submitter.value === "Login") {
        fetch('/api/authentication/login/', {
          method: 'post',
          body: JSON.stringify(account),
          headers: {
              'Content-Type': 'application/json'
          }
        }).then(response => response.json())
            .then(token => {
          if (token.result.access_token){
              login(token);
              this.props.update_login(true);
          }
          else {
                alert('Bad Username or Password');
          }
        })
      }
    }
  
    render() {
      if (this.props.logged_in) {
         return <Redirect to='/3stat' />;
      }
      return (
        <form onSubmit={this.handleSubmit}>
          <label>
            Email:
            <input name="email" type="text" value={this.state.email} onChange={this.handleChange} />
          </label>
          <br></br>
          <label>
            Phone #:
            <input name="phone" type="text" value={this.state.phone} onChange={this.handleChange} />
          </label>
          <br></br>
          <label>
            Password:
            <input name="password" type="password" value={this.state.password} onChange={this.handleChange} />
          </label>
          <br></br>
          <input type="submit" value="Sign Up" /><input type="submit" value="Login" />
        </form>
      );
    }
  }
  
  export default SignUp;