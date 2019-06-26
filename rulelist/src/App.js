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
        { title: 'Witness List',
          field: 'witness-list',
          type:'date',
          render: rowData => <span>{this.displayDate(rowData['witness-list'])}</span>,
          editable: 'onUpdate' },
        { title: 'Scheduling Conference',
          field: 'scheduling-conference',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData['scheduling-conference'])}</span>,
          editable: 'onUpdate'
        },
        { title: 'Request PTIs',
          field: 'defense-request-ptis',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData['defense-request-ptis'])}</span>,
          editable: 'onUpdate' },
        { title: 'Conduct PTIs',
          field: 'defense-conduct-ptis',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData['defense-conduct-ptis'])}</span>,
          editable: 'onUpdate' },
        { title: 'Witness PTIs',
          field: 'witness-ptis',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData['witness-ptis'])}</span>,
          editable: 'onUpdate' },
        { title: 'Scientific Evidence',
          field: 'scientific-evidence',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData['scientific-evidence'])}</span>,
          editable: 'onUpdate' },
        { title: 'Pretrial Motion Filing',
          field: 'pretrial-motion-filing',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData['pretrial-motion-filing'])}</span>,
          editable: 'onUpdate' },
        { title: 'Pretrial Conference',
          field: 'pretrial-conference',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData['pretrial-conference'])}</span>,
          editable: 'onUpdate' },
        { title: 'Final Witness List',
          field: 'final-witness-list',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData['final-witness-list'])}</span>,
          editable: 'onUpdate' },
        { title: 'Need for Interpreter',
          field: 'need-for-interpreter',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData['need-for-interpreter'])}</span>,
          editable: 'onUpdate' },
        { title: 'Plea Agreement',
          field: 'plea-agreement',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData['plea-agreement'])}</span>,
          editable: 'onUpdate' },
        { title: 'Trial',
          field: 'trial',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData['trial'])}</span>,
          editable: 'onUpdate' },
      ],
      tableData: [],
      jsonData: []
    }
  }

  displayDate(date) {
    /* Displays a date as M/D/YYYY.
    * param date: either Date or string
    * */

    let realDate = new Date();
    if (date) {
      if (typeof(date) === 'string') {
        realDate = new Date(date);
      } else {
        realDate = date;
      }

      // Could use Moment.js here instead...
      const day = realDate.getDate().toString();
      const month = (realDate.getMonth() + 1).toString();
      const year = realDate.getFullYear().toString();

      const dateString = month.concat('/', day, '/', year)

      return dateString;
    } else {
      return '';
    }
  }

  populateTable(cases) {

    // Save JSON Data to state
    this.setState({jsonData : cases});

    // Populate table with data
    let dataArray = [];
    cases.forEach(function(caseJSON){
      let row = {};

      // Populate basic case data
      row['defendant'] = caseJSON['defendant'];
      row['case_number'] = caseJSON['case_number'];
      row['judge'] = caseJSON['judge'];
      row['defense_attorney'] = caseJSON['defense_attorney'];
      row['notes'] = caseJSON['notes'];


      // Populate deadlines for case
      const deadlines = caseJSON['deadline_set']
      deadlines.forEach(function(deadline){
        const key = deadline['type'];
        // row[key] = deadline['datetime'].slice(0, 10); // FIXME Table needs to be tweaked to view date
        row[key] = new Date(deadline['datetime']);  // TODO: This is not recommended. Better to use Moment.js or roll our own
      });

      dataArray.push(row);
    });

    // Save table data to state
    this.setState(
      {tableData: dataArray}
    )
  }

  fetchCases() {
    return fetch("/api/cases/")
      .then(response => response.json())
      .then(cases => this.populateTable(cases))
  }

  putData(data) {
    // console.log('Data sent to /api/cases/ for update');
    // console.log(data);
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

  componentDidMount() {
    this.fetchCases();
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
                  // console.log('Update called');

                  // standard row update behavior
                  const data = this.state.tableData;
                  const index = data.indexOf(oldData);
                  data[index] = newData;

                  // final part of standard row update behavior
                  this.setState({ data }, () => resolve());

                  // update json data from newData
                  let dataToSend = this.state.jsonData[index];
                  // EDITABLE FIELDS TODO move to constants.js later
                  // Judge
                  // Defense
                  // Notes

                  dataToSend['judge'] = newData['judge'];
                  dataToSend['defense_attorney'] = newData['defense-attorney'];
                  dataToSend['notes'] = newData['notes'];


                  // console.log('dataToSend');
                  // console.log(dataToSend);

                  // Copy dates from deadlines to data that will be sent in request
                  this.state.columns.forEach(function(data) {
                    // console.log(data);
                    if (data.type === 'date' && data.editable === 'onUpdate') {
                      const deadlineIndex = dataToSend.deadline_set.findIndex(item => {
                        return item.type === data.field
                      });

                      /* TODO: Will not update deadline not found because it was not included in state.jsonData
                          This will be a problem when we want to enter a deadline that is currently blank.
                      */
                      if (deadlineIndex >= 0) {
                        if (oldData[data.field] !== newData[data.field]) {
                          dataToSend.deadline_set[deadlineIndex].datetime = newData[data.field];
                        }
                      }
                    }
                  });

                  this.putData(dataToSend);

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
