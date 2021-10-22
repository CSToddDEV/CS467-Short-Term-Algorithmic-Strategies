import React from 'react';

function Unsubscribe() {
    return (
      <div className="unsubscribe">
        <h1>Unsubscribe</h1>
        <h3>Enter an email or phone number to unsubscribe</h3>
        <UnsubscribeForm />
      </div>
    );
  }

  class UnsubscribeForm extends React.Component {
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
  
  export default Unsubscribe;