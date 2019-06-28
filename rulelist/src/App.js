import React, { Component } from 'react'
import ReactDOM from 'react-dom'
import TextField, {HelperText, Input} from '@material/react-text-field';
import MaterialIcon from '@material/react-material-icon';
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
          editable: 'never'},
        { title: 'Defense',
          field: 'defense-attorney' ,
          editable: 'never' },

        { title: 'Witness List',
          field: 'witness-list',
          type:'date',
          render: rowData => <span>{this.displayDate(rowData['witness-list'])}</span>,
          editable: 'never' },
        { title: 'Scheduling Conference',
          field: 'scheduling-conference',
          type: 'date',
          render: rowData => this.displayDate(rowData['scheduling-conference']),
          editable: 'never'
        },
        { title: 'Request PTIs',
          field: 'defense-request-ptis',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData['defense-request-ptis'])}</span>,
          editable: 'never' },
        { title: 'Conduct PTIs',
          field: 'defense-conduct-ptis',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData['defense-conduct-ptis'])}</span>,
          editable: 'never' },
        { title: 'Witness PTIs',
          field: 'witness-ptis',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData['witness-ptis'])}</span>,
          editable: 'never' },
        { title: 'Scientific Evidence',
          field: 'scientific-evidence',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData['scientific-evidence'])}</span>,
          editable: 'never' },
        { title: 'Pretrial Motion Filing',
          field: 'pretrial-motion-filing',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData['pretrial-motion-filing'])}</span>,
          editable: 'never' },
        { title: 'Pretrial Conference',
          field: 'pretrial-conference',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData['pretrial-conference'])}</span>,
          editable: 'never' },
        { title: 'Final Witness List',
          field: 'final-witness-list',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData['final-witness-list'])}</span>,
          editable: 'never' },
        { title: 'Need for Interpreter',
          field: 'need-for-interpreter',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData['need-for-interpreter'])}</span>,
          editable: 'never' },
        { title: 'Plea Agreement',
          field: 'plea-agreement',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData['plea-agreement'])}</span>,
          editable: 'never' },
        { title: 'Trial',
          field: 'trial',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData['trial'])}</span>,
          editable: 'never' },
      ],
      tableData: [],
      jsonData: []
    }
  }

  formatDate(date) {
    // Could use Moment.js here instead...
    const day = date.getDate().toString();
    const month = (date.getMonth() + 1).toString();
    const year = date.getFullYear().toString();

    return month.concat('/', day, '/', year)
  }

  displayDate(date) {
    /* Displays a date as M/D/YYYY.
    * param date: either Date or string in ISO format (e.g., 2019-06-28T22:13:06Z)
    * */

    let realDate = new Date();
    if (date) {
      if (typeof (date) === 'string') {
        realDate = new Date(date);
      } else {
        realDate = date;
      }
      return <span style={{backgroundColor: this.getDateBgColor(realDate)}}>{this.formatDate(realDate)}</span>;
    } else {
      return '';
    }
  }

  getDateBgColor(dueDate) {
    const today = new Date();
    const daysLeft = daysBetween(today, dueDate);

    if (5 < daysLeft) {
      return bgColors['OnTrack'];
    } else if (2 < daysLeft <= 5) {
      return bgColors['InTrouble'];
    } else if (daysLeft <= 2) {
      return bgColors['Urgent'];
    } else {
      return bgColors['Default'];
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
      row['case-number'] = caseJSON['case_number'];
      row['judge'] = caseJSON['judge'];
      row['defense-attorney'] = caseJSON['defense_attorney'];
      row['notes'] = caseJSON['notes'];
      row['status'] = 'good';

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

  setNotes(rowData, value) {
      rowData['notes'] = value;
      this.forceUpdate();
  }

  putNotes(rowData) {
      let json = this.state.jsonData[this.state.tableData.indexOf(rowData)];
      json['notes'] = rowData['notes'];
      this.putData(json).then(onfulfilled => alert('Saved!'))
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
        detailPanel={[{
            tooltip: 'Notes',
            render:rowData => {
            return <div>
        <TextField
          // helperText={<HelperText>Save</HelperText>}
          onTrailingIconSelect={() => {this.putNotes(rowData)}}
          trailingIcon={<MaterialIcon aria-label="Save" role="button" icon="done" hasRipple={true}/>}
        ><Input
            // disableUnderline={ true }
            value={ rowData['notes'] }
            onChange={(e) => this.setNotes(rowData, e.currentTarget.value)} />
        </TextField>
      </div>
        }}]}
      />
    )
  }
}

const bgColors = {
  "Expired": "C0C0C0", // light gray
  "Completed": "66B2FF", // light blue
  "OnTrack": "66FF66", // light green
  "InTrouble": "FFFF66", // light yellow
  "Urgent": "FF6666", // light red
  "Default": "FFFFFF" // white
}

// Per this source
// https://stackoverflow.com/questions/542938/how-do-i-get-the-number-of-days-between-two-dates-in-javascript
function treatAsUTC(date) {
    let result = new Date(date);
    result.setMinutes(result.getMinutes() - result.getTimezoneOffset());
    return result;
}

function daysBetween(startDate, endDate) {
    const millisecondsPerDay = 24 * 60 * 60 * 1000;
    return (treatAsUTC(endDate) - treatAsUTC(startDate)) / millisecondsPerDay;
}

export default App;
