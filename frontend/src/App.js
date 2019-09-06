import React from 'react'
import Tabs from 'muicss/lib/react/tabs';
import Tab from 'muicss/lib/react/tab';

import RuleList from './RuleList'
import UpcomingDeadlines from './UpcomingDeadlines'

class App extends React.Component {

  constructor(props) {
       super(props);

       this.state = {
            position: 0,
            is_supervisor: false
       }
  }

  fetchUser() {
       return fetch("/api/user/")
            .then(response => response.json())
            .then(userData => this.saveUserData(userData))
  }

    saveUserData(userData) {
        this.setState({
            position:userData[0]['position'],
            is_supervisor:userData[0]['is_supervisor']
        })
    }

    componentDidMount() {
        this.fetchUser();
    }

    renderStaffRuleList() {
        return <Tab value="pane-3" label="Staff Rule List">
                    <RuleList/>
               </Tab>
    }

    renderStaffDeadlines() {
        return <Tab value="pane-4" label="Staff Deadlines">
                    <UpcomingDeadlines/> 
               </Tab>
    }

  render() {
      const DEVELOPER = 99;
      let staffRuleList;
      let staffDeadlines;

      if (this.state.is_supervisor || this.state.position === DEVELOPER) {
          staffRuleList = this.renderStaffRuleList();
          staffDeadlines = this.renderStaffDeadlines();
      }


      return (
      <Tabs justified={true}>
        <Tab value="pane-1" label="Rule List">
          <RuleList/>
        </Tab>
          { staffRuleList }
        <Tab value="pane-2" label="Upcoming Deadlines">
          <UpcomingDeadlines/>
        </Tab>
          { staffDeadlines }
      </Tabs>
    )
  }
}

export default App;
