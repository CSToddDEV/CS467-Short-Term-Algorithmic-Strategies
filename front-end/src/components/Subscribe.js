import React from 'react';

function Subscribe() {
    return (
      <div className="subscribe content">
        <h1>Subscribe</h1>
        <h3>Enter an email and/or phone number (text) to receive buy/sell signals</h3>
        <SubscribeForm />
      </div>
    );
  }

  class SubscribeForm extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        email: '',
        phone: ''
      }
  
      this.handleChange = this.handleChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
    }
  
    handleChange(event) {
      const name = event.target.name;

      this.setState({[name]: event.target.value});
    }
  
    handleSubmit(event) {
      alert('Email submitted: ' + this.state.email + ' / Phone # submitted: ' + this.state.phone);
      event.preventDefault();
    }
  
    render() {
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
          <input type="submit" value="Submit" />
        </form>
      );
    }
  }
  
  export default Subscribe;