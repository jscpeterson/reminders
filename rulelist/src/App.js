import React from 'react'
import MaterialTable from 'material-table'
import Cookies from 'js-cookie'

class App extends React.Component {
  constructor(props) {
    super(props);

    // EDITABLE FIELDS TODO move to constants.js later
      // Judge
      // Defense
      // Notes

    this.state = {
      columns: [
        { title: 'Defendant',
            field: 'defendant',
            editable: 'never' },
        { title: 'CR#',
            field: 'case-number',
            editable: 'never' },
        { title: 'Judge',
            field: 'judge' ,
            editable: 'onUpdate'},
        { title: 'Defense',
            field: 'defense-attorney' ,
            editable: 'onUpdate' },

          // TODO Notes cell should be larger
        { title: 'Notes', field: 'notes', editable: 'onUpdate' },

          // TODO Deadline cell data isn't visible until a column is selected
        { title: 'Witness List',
            field: 'witness-list',
            type:'date',
            editable: 'onUpdate' },
        { title: 'Scheduling Conference',
            field: 'scheduling-conference',
            type: 'date',
            editable: 'onUpdate' },
        { title: 'Request PTIs',
            field: 'defense-request-ptis',
            type: 'date',
            editable: 'onUpdate' },
        { title: 'Conduct PTIs',
            field: 'defense-conduct-ptis',
            type: 'date',
            editable: 'onUpdate' },
        { title: 'Witness PTIs',
            field: 'witness-ptis',
            type: 'date',
            editable: 'onUpdate' },
        { title: 'Scientific Evidence',
            field: 'scientific-evidence',
            type: 'date',
            editable: 'onUpdate' },
        { title: 'Pretrial Motion Filing',
            field: 'pretrial-motion-filing',
            type: 'date',
            editable: 'onUpdate' },
        { title: 'Pretrial Conference',
            field: 'pretrial-conference',
            type: 'date',
            editable: 'onUpdate' },
        { title: 'Final Witness List',
            field: 'final-witness-list',
            type: 'date',
            editable: 'onUpdate' },
        { title: 'Need for Interpreter',
            field: 'need-for-interpreter',
            type: 'date',
            editable: 'onUpdate' },
        { title: 'Plea Agreement',
            field: 'plea-agreement',
            type: 'date',
            editable: 'onUpdate' },
        { title: 'Trial',
            field: 'trial',
            type: 'date',
            editable: 'onUpdate' },
      ],

      tableData: [],

      jsonData: []

    }
  }

  populateJson(cases) {

    // Save JSON Data
    this.setState({jsonData : cases});

    let dataArray = [];

    cases.forEach(function(casejson){
        let row = {};

        // Populate basic data for table
        row['defendant'] = casejson['defendant'];
        row['case_number'] = casejson['case_number'];
        row['judge'] = casejson['judge'];
        row['defense_attorney'] = casejson['defense_attorney'];
        row['notes'] = casejson['notes'];

        const deadlines = casejson['deadline_set']
        
        deadlines.forEach(function(deadline){
                const key = deadline['type'];
                row[key] = deadline['datetime'].slice(0, 10); // FIXME Table needs to be tweaked to view date
            });

        dataArray.push(row);
    });

    this.setState(
        {tableData: dataArray}
    )
  }

  fetchJson() {
    return fetch("/api/cases/")
          .then(response => response.json())
          .then(cases => this.populateJson(cases))
  }

  updateData(data) {
      console.log('Data sent to /api/cases/ for update');
      console.log(data);
      let pk = data['id'];
      let url = `/api/cases/${pk}/`;
      return fetch(url, {
          method: 'PUT',
          body: JSON.stringify(data),
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': Cookies.get('csrftoken')
          }
    })
  }

  updateDeadline(data) {
      let pk = data['id'];
      let url = `/api/deadlines/${pk}/`;
      return fetch(url, {
          method: 'PUT',
          body: JSON.stringify(data),
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': Cookies.get('csrftoken')
          }
    })
  }

  getDeadlineIdFromType(data, caseNumber, type) {
      // Returns deadline ID in database given the deadline type
      // ('scheduling-conference') =>

      const theCase = data.find(item => {
          return item.case_number === caseNumber
      });

      const deadline = theCase.deadline_set.find(item => {
          return item.type === type
      });
      return deadline.id;
  }

  componentDidMount() {
    this.fetchJson();
  }

  render() {
    return (
      <MaterialTable
        title="Rule List"
        columns={this.state.columns}
        data={this.state.tableData}
        options={{
            pageSize: 10
        }}
        editable={{
          onRowUpdate: (newData, oldData) =>
              new Promise((resolve, reject) => {
              setTimeout(() => {
                {
                  // standard row update behavior
                  const data = this.state.tableData;
                  const index = data.indexOf(oldData);
                  data[index] = newData;

                  // update json data from newData
                  //let json = this.state.jsonData[index];
                    let json = {};
                  // EDITABLE FIELDS TODO move to constants.js later
                    // Judge
                    // Defense
                    // Notes

                    json['id'] = this.state.jsonData[index]['id'];
                  json['judge'] = newData['judge'];
                  json['defense_attorney'] = newData['defense-attorney'];
                  json['notes'] = newData['notes'];
                  this.updateData(json);

                  // update deadlines
                    console.log('newData');
                    console.log(newData);

                    console.log('oldData');
                    console.log(oldData);

                    console.log('jsonData');
                    console.log(this.state.jsonData);

                    if (oldData['scheduling-conference'] !== newData['scheduling-conference']) {
                        const deadlineData = {};
                        deadlineData['id'] = this.getDeadlineIdFromType(
                            this.state.jsonData,
                            newData['case-number'],
                            'scheduling-conference'
                        );
                        deadlineData['datetime'] = newData['scheduling-conference']
                        this.updateDeadline(deadlineData)
                    }

                  // final part of standard row update behavior
                  this.setState({ data }, () => resolve());
                }
                resolve()
              }, 1000)
            }),
        }}
      />
    )
  }
}

export default App;
