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
        password: '',
        submitError: false
      }
  
      this.handleChange = this.handleChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
    }
  
    handleChange(event) {
      const name = event.target.name;

      this.setState({[name]: event.target.value});
    }
  
    handleSubmit(event) {
      event.preventDefault();
      let account = {
          'email' : this.state.email,
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
        .catch((error) => {
          console.log(error);
          this.setState({
            submitError: true
          });
        });
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
        .catch((error) => {
          console.log(error);
          this.setState({
            submitError: true
          });
        });
      }
    }
  
    render() {
      if (this.props.logged_in) {
         return <Redirect to='/3stat' />;
      }
      return (
        <div className="signupContent">
          <form onSubmit={this.handleSubmit}>
            <label>
              Email:
              <input name="email" type="text" value={this.state.email} onChange={this.handleChange} />
            </label>
            <br></br>
            <label>
              Password:
              <input name="password" type="password" value={this.state.password} onChange={this.handleChange} />
            </label>
            <br></br>
            <input type="submit" value="Sign Up" /><input type="submit" value="Login" />
          </form>
          {this.state.submitError ? <p className="errorMsg">Either a server error has occurred or incorrect inputs have been entered. Please ensure that a valid email and/or phone number have been entered.</p> : null}
        </div>
      );
    }
  }
  
  export default SignUp;