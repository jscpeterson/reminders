import React from 'react'
import Tabs from 'muicss/lib/react/tabs';
import Tab from 'muicss/lib/react/tab';

import RuleList from './RuleList'
import UpcomingDeadlines from './UpcomingDeadlines'
import ManagementTable from './ManagementTable'

class App extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            position:0
        }
    }

    fetchUser() {
        return fetch("/api/user/")
            .then(response => response.json())
            .then(userData => this.saveUserData(userData))
    }

    saveUserData(userData) {
        this.setState({position:userData[0]['position']})
    }

    componentDidMount() {
        this.fetchUser();
    }

    renderTab() {
        return <Tab value="pane-2" label="Management">
                    <ManagementTable/>
               </Tab>
    }

    render() {
        let tab;
        const SUPERVISOR = 1;

        if (this.state.position === SUPERVISOR) {
            tab = this.renderTab();
        }

        return (
            <Tabs justified={true}>
                <Tab value="pane-1" label="Rule List">
                    <RuleList/>
                </Tab>
                <Tab value="pane-2" label="Upcoming Deadlines">
                    <UpcomingDeadlines/>
                </Tab>
                { tab }
            </Tabs>
    )
  }
}

export default App;
