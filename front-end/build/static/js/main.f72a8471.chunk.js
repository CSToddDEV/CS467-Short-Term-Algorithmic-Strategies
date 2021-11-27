(this["webpackJsonpmy-react-app"]=this["webpackJsonpmy-react-app"]||[]).push([[0],{36:function(e,t,a){},51:function(e,t,a){"use strict";a.r(t);var s=a(1),n=a.n(s),r=a(26),i=a.n(r),c=a(31),o=(a(36),a(6)),l=a(0);var h=function(e){return Object(l.jsx)("nav",{children:Object(l.jsxs)("ul",{className:"nav",children:[Object(l.jsx)("li",{className:"navUnit",children:Object(l.jsx)(o.b,{exact:!0,activeClassName:"selectedLink",className:"navLink",to:"/3stat",children:"Home"})}),Object(l.jsx)("li",{className:"navUnit",children:Object(l.jsx)(o.b,{exact:!0,activeClassName:"selectedLink",className:"navLink",to:"/3stat/about",children:"About"})}),e.logged_in?Object(l.jsx)("li",{className:"navUnit",children:Object(l.jsx)(o.b,{exact:!0,activeClassName:"selectedLink",className:"navLink",to:"/3stat/unsubscribe",children:"Unsubscribe"})}):null,e.logged_in?Object(l.jsx)("li",{className:"navUnit",children:Object(l.jsx)(o.b,{exact:!0,activeClassName:"selectedLink",className:"navLink",to:"/3stat/data",children:"Signal Data"})}):null,e.logged_in?Object(l.jsx)("li",{className:"navUnit",children:Object(l.jsx)(o.b,{exact:!0,activeClassName:"selectedLink",className:"navLink",to:"/3stat/portfolio",children:"Portfolio"})}):null,Object(l.jsx)("li",{className:"navUnit",children:Object(l.jsx)(o.b,{exact:!0,activeClassName:"selectedLink",className:"navLink",to:"/3stat/performance",children:"Performance"})}),e.logged_in?null:Object(l.jsx)("li",{className:"navUnit",children:Object(l.jsx)(o.b,{exact:!0,activeClassName:"selectedLink",className:"navLink",to:"/3stat/signup",children:"Sign Up"})}),e.logged_in?Object(l.jsx)("button",{onClick:function(){Y(),e.update_login(!1)},children:"Logout"}):null]})})},d=a(2);var b=function(){return Object(l.jsxs)("div",{className:"home content",children:[Object(l.jsx)("h1",{children:"3STAT"}),Object(l.jsx)("h3",{children:"Welcome to the 3X ETF Algorithmic Trader!"})]})};var j=function(){return Object(l.jsxs)("div",{className:"about_content",children:[Object(l.jsx)("h1",{children:"About 3STAT"}),Object(l.jsxs)("p",{children:["Inflation is actively outpacing most traditional investments.  The US bond market is falling apart.  The global economy is extremely volatile.   We see wealth being hoarded by the rich and watch as policy is created by the highest bidder.",Object(l.jsx)("br",{}),Object(l.jsx)("br",{}),"If your money is not working for you, it is actively working against you.",Object(l.jsx)("br",{}),Object(l.jsx)("br",{}),"Now is the rise of the Retail Investor.  Investor\u2019s looking to take charge of their finances, their future, their hope.  But in the world of Market Makers and Big Money, many Retail Investors are looking for direction.",Object(l.jsx)("br",{}),Object(l.jsx)("br",{}),"Welcome to 3STAT.",Object(l.jsx)("br",{}),Object(l.jsx)("br",{}),"The 3STAT Algorithm is a momentum-based multi-resolution trading algorithm with aggressive risk management built in.  The 3STAT Algorithm focuses on a curated list of 3X ETFs, with monthly universe selection utilizing volatility.  With the leveraged power of the 3X weighted ETFS, and the aggressive risk management, the 3STAT Algorithm aims to deliver mighty gains with short-term trades.",Object(l.jsx)("br",{}),Object(l.jsx)("br",{}),"But what sets 3STAT Algorithm apart from every other Algorithmic Trader out there is its approachability provided by the 3STAT web-app.  With an interface that is navigable even for luddites, the 3STAT web-app is designed and built to be approachable for traders of all types.  You may view the performance of the 3STAT Algorithm over select periods from the performance page.  You will also be able to see that performance compared to classic benchmarks during those same periods.  All of this is provided for free to help users make the best decision for their portfolio that they can.",Object(l.jsx)("br",{}),Object(l.jsx)("br",{}),"If you choose to sign up and become a free subscriber, you will be emailed whenever the 3STAT Algorithm has produced a new buy or sell signal.  This allows 3STAT subscribers to choose to mimic the buy and sell patterns of the 3STAT Algorithm, and reap what rewards come with it.",Object(l.jsx)("br",{}),Object(l.jsx)("br",{}),Object(l.jsx)("br",{}),Object(l.jsx)("br",{}),Object(l.jsx)("span",{className:"disclaimer",children:"A new type of Investor calls for a new type of tool.  3STAT, buy in to your future."}),Object(l.jsx)("br",{}),Object(l.jsx)("br",{}),Object(l.jsx)("br",{}),Object(l.jsx)("br",{}),Object(l.jsx)("br",{}),Object(l.jsx)("br",{}),Object(l.jsxs)("span",{className:"footer",children:["3STAT is a short-term algorithmic trading strategy project by Dylan Bodvig, Doug Hughes, Ryan Patton, Calvin Todd, and Timothy Turnbaugh for the Oregon State University Fall 2021 Computer Science Capstone class.",Object(l.jsx)("br",{}),Object(l.jsx)("br",{}),Object(l.jsx)("span",{className:"disclaimer",children:"Disclaimer:"})," Nothing on this website is intended to represent financial advice.  Investing in stocks, bonds, exchange traded funds, mutual funds, and money market funds involve risk of loss.  Loss of principal is possible. Some high risk investments may use leverage, which will accentuate gains & losses. A security\u2019s or an algorithm\u2019s past investment performance is not a guarantee or predictor of future investment performance."]})]})]})},u=a(12),m=a(7),p=a(8),O=a(5),x=a(10),g=a(9);var v=function(e){Object(x.a)(a,e);var t=Object(g.a)(a);function a(e){var s;return Object(m.a)(this,a),s=t.call(this,e),console.log("Subscribe"),console.log(e),s.state={email:"",phone:"",password:"",submitError:!1},s.handleChange=s.handleChange.bind(Object(O.a)(s)),s.handleSubmit=s.handleSubmit.bind(Object(O.a)(s)),s}return Object(p.a)(a,[{key:"handleChange",value:function(e){var t=e.target.name;this.setState(Object(u.a)({},t,e.target.value))}},{key:"handleSubmit",value:function(e){var t=this;e.preventDefault();var a={email:this.state.email,phone:this.state.phone,password:this.state.password};"Sign Up"===e.nativeEvent.submitter.value?fetch("/api/authentication/register/",{method:"post",body:JSON.stringify(a),headers:{"Content-Type":"application/json"}}).then((function(e){return e.json()})).then((function(e){e.result.access_token?(H(e),t.props.update_login(!0)):alert("Bad Username or Password, or Already Registered")})).catch((function(e){console.log(e),t.setState({submitError:!0})})):"Login"===e.nativeEvent.submitter.value&&fetch("/api/authentication/login/",{method:"post",body:JSON.stringify(a),headers:{"Content-Type":"application/json"}}).then((function(e){return e.json()})).then((function(e){e.result.access_token?(H(e),t.props.update_login(!0)):alert("Bad Username or Password")})).catch((function(e){console.log(e),t.setState({submitError:!0})}))}},{key:"render",value:function(){return this.props.logged_in?Object(l.jsx)(d.a,{to:"/3stat"}):Object(l.jsxs)("div",{className:"signupContent",children:[Object(l.jsxs)("form",{onSubmit:this.handleSubmit,children:[Object(l.jsxs)("label",{children:["Email:",Object(l.jsx)("input",{name:"email",type:"text",value:this.state.email,onChange:this.handleChange})]}),Object(l.jsx)("br",{}),Object(l.jsxs)("label",{children:["Phone #:",Object(l.jsx)("input",{name:"phone",type:"text",value:this.state.phone,onChange:this.handleChange})]}),Object(l.jsx)("br",{}),Object(l.jsxs)("label",{children:["Password:",Object(l.jsx)("input",{name:"password",type:"password",value:this.state.password,onChange:this.handleChange})]}),Object(l.jsx)("br",{}),Object(l.jsx)("input",{type:"submit",value:"Sign Up"}),Object(l.jsx)("input",{type:"submit",value:"Login"})]}),this.state.submitError?Object(l.jsx)("p",{className:"errorMsg",children:"Either a server error has occurred or incorrect inputs have been entered. Please ensure that a valid email and/or phone number have been entered."}):null]})}}]),a}(n.a.Component),f=function(e){return Object(l.jsxs)("div",{className:"subscribe content",children:[Object(l.jsx)("h1",{children:"Sign Up"}),Object(l.jsx)("h3",{children:"Enter an email and a phone number (text, optional), and a password to sign up for 3STAT"}),Object(l.jsx)(v,{logged_in:e.logged_in,update_login:e.update_login})]})};var y=function(e){Object(x.a)(a,e);var t=Object(g.a)(a);function a(e){var s;return Object(m.a)(this,a),(s=t.call(this,e)).state={email:"",phone:""},s.handleChange=s.handleChange.bind(Object(O.a)(s)),s.handleSubmit=s.handleSubmit.bind(Object(O.a)(s)),s}return Object(p.a)(a,[{key:"handleChange",value:function(e){var t=e.target.name;this.setState(Object(u.a)({},t,e.target.value))}},{key:"handleSubmit",value:function(e){alert("Email submitted: "+this.state.email+" / Phone # submitted: "+this.state.phone),e.preventDefault()}},{key:"render",value:function(){return Object(l.jsxs)("form",{onSubmit:this.handleSubmit,children:[Object(l.jsxs)("label",{children:["Email:",Object(l.jsx)("input",{name:"email",type:"text",value:this.state.email,onChange:this.handleChange})]}),Object(l.jsx)("br",{}),Object(l.jsxs)("label",{children:["Phone #:",Object(l.jsx)("input",{name:"phone",type:"text",value:this.state.phone,onChange:this.handleChange})]}),Object(l.jsx)("br",{}),Object(l.jsx)("input",{type:"submit",value:"Submit"})]})}}]),a}(n.a.Component),S=function(){return Object(l.jsxs)("div",{className:"unsubscribe content",children:[Object(l.jsx)("h1",{children:"Unsubscribe"}),Object(l.jsx)("h3",{children:"Enter an email or phone number to unsubscribe"}),Object(l.jsx)(y,{})]})},k=["Tracked Ticker","Date","Signal","% invested"];var w=function(e){Object(x.a)(a,e);var t=Object(g.a)(a);function a(e){var s;return Object(m.a)(this,a),(s=t.call(this,e)).state={signals:[],isLoading:!0,serverError:!1},s}return Object(p.a)(a,[{key:"componentDidMount",value:function(){var e=this;B("/3stat/signals/",{method:"get",headers:{"Content-Type":"application/json"}}).then((function(e){return e.json()})).then((function(t){e.setState({signals:t,isLoading:!1})})).catch((function(t){console.log(t),e.setState({serverError:!0,isLoading:!1})}))}},{key:"generateHeaders",value:function(){var e=[];return this.props.headers.forEach((function(t){e.push(Object(l.jsx)("th",{children:t}))})),e}},{key:"generateRows",value:function(){var e=[];return console.log("ROWS",this.state.signals.result),this.state.signals.result.forEach((function(t){var a=[];a.push(Object(l.jsx)("td",{children:t.ticker})),a.push(Object(l.jsx)("td",{children:t.date})),a.push(Object(l.jsx)("td",{children:t.signal})),a.push(Object(l.jsx)("td",{children:t.total_invested+"%"})),e.push(Object(l.jsx)("tr",{children:a},t.id))})),e}},{key:"render",value:function(){if(this.state.isLoading)return Object(l.jsx)("p",{children:"Data is loading..."});if(this.state.serverError)return Object(l.jsx)("h3",{children:"Server error - unable to retrieve the data"});var e=this.generateHeaders(),t=this.generateRows();return Object(l.jsxs)("table",{children:[Object(l.jsx)("thead",{children:Object(l.jsx)("tr",{children:e})}),Object(l.jsx)("tbody",{children:t})]})}}]),a}(n.a.Component),C=function(){return Object(l.jsxs)("div",{className:"data content",children:[Object(l.jsx)("h1",{children:"Signal Data"}),Object(l.jsx)(w,{headers:k})]})},N=a(29),T={fontSize:"5px",fontFamily:"sans-serif"},_=["#86e39f","#11782c","#65d900","#789163"],A=function(e){Object(x.a)(a,e);var t=Object(g.a)(a);function a(e){var s;return Object(m.a)(this,a),(s=t.call(this,e)).state={ticker:"",percent_invested:0,isLoading:!0,dataAvailable:!0,serverError:!1},s}return Object(p.a)(a,[{key:"componentDidMount",value:function(){var e=this;B("/3stat/signals/",{method:"get",headers:{"Content-Type":"application/json"}}).then((function(e){return e.json()})).then((function(t){0===t.result.length?e.setState({dataAvailable:!1,isLoading:!1}):(console.log(t.result.at(-1).ticker),e.setState({ticker:t.result.at(-1).ticker,percent_invested:t.result.at(-1).total_invested,isLoading:!1}))})).catch((function(t){console.log(t),e.setState({serverError:!0,isLoading:!1})}))}},{key:"makeGraphData",value:function(){var e=[],t=0,a=100-this.state.percent_invested;return a>0&&(e.push({title:"CASH",value:a,color:_[t]}),t++),this.state.percent_invested>0&&e.push({title:this.state.ticker,value:this.state.percent_invested,color:_[t]}),e}},{key:"render",value:function(){return this.state.isLoading?Object(l.jsx)("h3",{children:"Data loading..."}):this.state.dataAvailable?this.state.serverError?Object(l.jsx)("h3",{children:"Server error - could not retrieve the requested data"}):Object(l.jsxs)("div",{className:"portfolio content",children:[Object(l.jsx)("h1",{children:"Current Portfolio Holdings"}),Object(l.jsx)(N.PieChart,{data:this.makeGraphData(),label:function(e){var t=e.x,a=e.y,s=e.dx,n=e.dy,r=e.dataEntry;return Object(l.jsx)("text",{x:t,y:a,dx:s,dy:n,"dominant-baseline":"central","text-anchor":"middle",style:{fontSize:"5px",fontFamily:"sans-serif"},children:Math.round(r.percentage)+"% "+r.title})},labelStyle:T,labelPosition:60,segmentsShift:.4,radius:45})]}):Object(l.jsx)("h3",{children:"No data currently available"})}}]),a}(n.a.Component),L=["2 Weeks","1 Month","3 Months","6 Months","1 Year"],M=new Map,E=(new Date).toDateString();var P=function(e){Object(x.a)(a,e);var t=Object(g.a)(a);function a(e){var s;return Object(m.a)(this,a),(s=t.call(this,e)).state={currentPeriod:"2 Weeks",startingCash:1e3,tempCash:1e3,isLoading:!0,dataAvailable:!0,serverError:!1},s.onClick=s.handleClick.bind(Object(O.a)(s)),s.onSubmit=s.handleSubmit.bind(Object(O.a)(s)),s.onChange=s.handleChange.bind(Object(O.a)(s)),s}return Object(p.a)(a,[{key:"componentDidMount",value:function(){var e=this;fetch("/3stat/stats/",{method:"get",headers:{"Content-Type":"application/json"}}).then((function(e){return e.json()})).then((function(t){0===t.result.length?e.setState({dataAvailable:!1,isLoading:!1}):e.setState({stats:t.result})})).then((function(){e.state.dataAvailable&&(M.set("2 Weeks",{period:"2 Weeks",rate_of_return:e.state.stats.at(4).rate_of_return,benchmark_ror:e.state.stats.at(4).benchmark_ror[0][0].ror,drawdown:e.state.stats.at(4).drawdown}),M.set("1 Month",{period:"1 Month",rate_of_return:e.state.stats.at(3).rate_of_return,benchmark_ror:e.state.stats.at(3).benchmark_ror[0][0].ror,drawdown:e.state.stats.at(3).drawdown}),M.set("3 Months",{period:"3 Months",rate_of_return:e.state.stats.at(2).rate_of_return,benchmark_ror:e.state.stats.at(2).benchmark_ror[0][0].ror,drawdown:e.state.stats.at(2).drawdown}),M.set("6 Months",{period:"6 Months",rate_of_return:e.state.stats.at(1).rate_of_return,benchmark_ror:e.state.stats.at(1).benchmark_ror[0][0].ror,drawdown:e.state.stats.at(1).drawdown}),M.set("1 Year",{period:"1 Year",rate_of_return:e.state.stats.at(0).rate_of_return,benchmark_ror:e.state.stats.at(0).benchmark_ror[0][0].ror,drawdown:e.state.stats.at(0).drawdown}),e.setState({isLoading:!1}))})).catch((function(t){console.log(t),e.setState({isLoading:!1,serverError:!0})}))}},{key:"handleClick",value:function(e){this.setState({currentPeriod:e.target.name})}},{key:"handleSubmit",value:function(e){e.preventDefault();var t=parseFloat(this.state.tempCash);Number.isNaN(t)||this.setState({startingCash:t})}},{key:"handleChange",value:function(e){this.setState({tempCash:e.target.value})}},{key:"generatePeriodHeaders",value:function(){var e=this,t=[];return L.forEach((function(a){a===e.state.currentPeriod?t.push(Object(l.jsx)("button",{className:"selectedBtn",name:a,onClick:e.onClick,children:a})):t.push(Object(l.jsx)("button",{name:a,onClick:e.onClick,children:a}))})),t}},{key:"setTwoDecimals",value:function(e){return(Math.round(100*e)/100).toFixed(2)}},{key:"buildMetricRow",value:function(e,t,a){var s="+";t<0&&(s="-",t*=-1);var n="-";return a&&(n=s+"$"+this.setTwoDecimals(t/100*this.state.startingCash).toString()),Object(l.jsxs)("tr",{children:[Object(l.jsx)("td",{children:e}),Object(l.jsx)("td",{children:s+t.toString()+"%"}),Object(l.jsx)("td",{children:n})]})}},{key:"generateMetricRows",value:function(){var e=[],t=M.get(this.state.currentPeriod);return e.push(this.buildMetricRow("3STAT Rate Of Return",t.rate_of_return,!0)),e.push(this.buildMetricRow("S&P 500 Rate of Return",t.benchmark_ror,!0)),e.push(this.buildMetricRow("Monthly Draw Down Percent",t.drawdown,!1)),e}},{key:"render",value:function(){var e=this.generatePeriodHeaders();if(this.state.isLoading)return Object(l.jsxs)("div",{className:"metricsView",children:[Object(l.jsxs)("form",{onSubmit:this.onSubmit,children:[Object(l.jsx)("label",{htmlFor:"startingCash",className:"performanceLabel",children:"Starting cash ($):"}),Object(l.jsx)("input",{name:"startingCash",type:"text",value:this.state.tempCash,onChange:this.onChange}),Object(l.jsx)("input",{type:"submit",value:"Set"})]}),Object(l.jsx)("br",{}),Object(l.jsxs)("div",{className:"periodTabs",children:[Object(l.jsx)("span",{className:"performanceLabel",children:"Time Period: "}),e]}),Object(l.jsxs)("p",{className:"periodsNote",children:["Time periods ending ",E]}),Object(l.jsxs)("table",{className:"metricsTable",children:[Object(l.jsx)("thead",{children:Object(l.jsxs)("tr",{children:[Object(l.jsx)("th",{children:"Metric"}),Object(l.jsx)("th",{children:"% change"}),Object(l.jsxs)("th",{children:["Dollar change ",Object(l.jsx)("br",{}),"(based on starting cash)"]})]})}),Object(l.jsx)("tbody",{children:"Data is Loading..."})]})]});if(this.state.dataAvailable){if(this.state.serverError)return Object(l.jsxs)("div",{className:"metricsView",children:[Object(l.jsxs)("form",{onSubmit:this.onSubmit,children:[Object(l.jsx)("label",{htmlFor:"startingCash",className:"performanceLabel",children:"Starting cash ($):"}),Object(l.jsx)("input",{name:"startingCash",type:"text",value:this.state.tempCash,onChange:this.onChange}),Object(l.jsx)("input",{type:"submit",value:"Set"})]}),Object(l.jsx)("br",{}),Object(l.jsxs)("div",{className:"periodTabs",children:[Object(l.jsx)("span",{className:"performanceLabel",children:"Time Period: "}),e]}),Object(l.jsxs)("p",{className:"periodsNote",children:["Time periods ending ",E]}),Object(l.jsxs)("table",{className:"metricsTable",children:[Object(l.jsx)("thead",{children:Object(l.jsxs)("tr",{children:[Object(l.jsx)("th",{children:"Metric"}),Object(l.jsx)("th",{children:"% change"}),Object(l.jsxs)("th",{children:["Dollar change ",Object(l.jsx)("br",{}),"(based on starting cash)"]})]})}),Object(l.jsx)("tbody",{children:Object(l.jsx)("tr",{children:Object(l.jsx)("td",{colspan:"3",children:"Server error - unable to retrieve the data"})})})]})]});var t=this.generateMetricRows();return Object(l.jsxs)("div",{className:"metricsView",children:[Object(l.jsxs)("form",{onSubmit:this.onSubmit,children:[Object(l.jsx)("label",{for:"startingCash",className:"performanceLabel",children:"Starting cash ($):"}),Object(l.jsx)("input",{name:"startingCash",type:"text",value:this.state.tempCash,onChange:this.onChange}),Object(l.jsx)("input",{type:"submit",value:"Set"})]}),Object(l.jsx)("br",{}),Object(l.jsxs)("div",{className:"periodTabs",children:[Object(l.jsx)("span",{className:"performanceLabel",children:"Time Period: "}),e]}),Object(l.jsxs)("p",{className:"periodsNote",children:["Time periods ending ",E]}),Object(l.jsxs)("table",{className:"metricsTable",children:[Object(l.jsx)("thead",{children:Object(l.jsxs)("tr",{children:[Object(l.jsx)("th",{children:"Metric"}),Object(l.jsx)("th",{children:"% change"}),Object(l.jsxs)("th",{children:["Dollar change ",Object(l.jsx)("br",{}),"(based on starting cash)"]})]})}),Object(l.jsx)("tbody",{children:t})]})]})}return Object(l.jsxs)("div",{className:"metricsView",children:[Object(l.jsxs)("form",{onSubmit:this.onSubmit,children:[Object(l.jsx)("label",{htmlFor:"startingCash",className:"performanceLabel",children:"Starting cash ($):"}),Object(l.jsx)("input",{name:"startingCash",type:"text",value:this.state.tempCash,onChange:this.onChange}),Object(l.jsx)("input",{type:"submit",value:"Set"})]}),Object(l.jsx)("br",{}),Object(l.jsxs)("div",{className:"periodTabs",children:[Object(l.jsx)("span",{className:"performanceLabel",children:"Time Period: "}),e]}),Object(l.jsxs)("p",{className:"periodsNote",children:["Time periods ending ",E]}),Object(l.jsxs)("table",{className:"metricsTable",children:[Object(l.jsx)("thead",{children:Object(l.jsxs)("tr",{children:[Object(l.jsx)("th",{children:"Metric"}),Object(l.jsx)("th",{children:"% change"}),Object(l.jsxs)("th",{children:["Dollar change ",Object(l.jsx)("br",{}),"(based on starting cash)"]})]})}),Object(l.jsx)("tbody",{children:Object(l.jsx)("tr",{children:Object(l.jsx)("td",{colspan:"3",children:"No data currently available"})})})]})]})}}]),a}(n.a.Component),D=function(e){return Object(l.jsxs)("div",{className:"performance content",children:[Object(l.jsx)("h1",{children:"Performance Metrics"}),Object(l.jsx)(P,{map:e})]})},R=function(){return Object(l.jsxs)("div",{className:"404",children:[Object(l.jsx)("h1",{children:"404"}),Object(l.jsx)("h3",{children:"The page does not exist. Please check the web address."})]})};var U=function(e){return Object(l.jsxs)(d.d,{children:[Object(l.jsx)(d.b,{exact:!0,path:"/3stat",component:b}),Object(l.jsx)(d.b,{exact:!0,path:"/3stat/about",component:j}),Object(l.jsx)(d.b,{exact:!0,path:"/3stat/signup",render:function(){return Object(l.jsx)(f,{logged_in:e.logged_in,update_login:e.update_login})}}),Object(l.jsx)(d.b,{exact:!0,path:"/3stat/unsubscribe",component:S}),Object(l.jsx)(d.b,{exact:!0,path:"/3stat/data",component:C}),Object(l.jsx)(d.b,{exact:!0,path:"/3stat/portfolio",component:A}),Object(l.jsx)(d.b,{exact:!0,path:"/3stat/performance",component:D}),Object(l.jsx)(d.b,{component:R})]})},F=a(30),W=Object(F.createAuthProvider)({getAccessToken:function(e){return e.result.access_token},storage:localStorage}),I=W.useAuth,B=W.authFetch,H=W.login,Y=W.logout;var $=function(){var e=I(),t=Object(s.useState)(e[0]),a=Object(c.a)(t,2),n=a[0],r=a[1];return Object(l.jsxs)("div",{className:"App",children:[Object(l.jsx)(h,{logged_in:n,update_login:r}),Object(l.jsx)(U,{logged_in:n,update_login:r})]})};i.a.render(Object(l.jsx)(o.a,{children:Object(l.jsx)($,{})}),document.getElementById("root"))}},[[51,1,2]]]);
//# sourceMappingURL=main.f72a8471.chunk.js.map