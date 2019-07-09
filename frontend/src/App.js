import React from 'react'
import Tabs from 'muicss/lib/react/tabs';
import Tab from 'muicss/lib/react/tab';

import RuleList from './RuleList'
import UpcomingDeadlines from './UpcomingDeadlines'

class App extends React.Component {

  render() {
    return (
      <Tabs justified={true}>
        <Tab value="pane-1" label="Rule List">
          <RuleList/>
        </Tab>
        <Tab value="pane-2" label="Upcoming Deadlines">
          <UpcomingDeadlines/>
        </Tab>
      </Tabs>
    )
  }
}

export default App;
