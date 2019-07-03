import React from 'react'
import TextField, {HelperText, Input} from '@material/react-text-field';
import MaterialIcon from '@material/react-material-icon';
import MaterialTable from 'material-table'
import Cookies from 'js-cookie'

class App extends React.Component {
  constructor(props) {
    super(props);

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
          render: rowData => <span>{this.displayDate(rowData['scheduling-conference'])}</span>,
          editable: 'never'
        },
        { title: 'PTIs Requested',
          field: 'defense-request-ptis',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData['defense-request-ptis'])}</span>,
          editable: 'never' },
        { title: 'PTIs Conducted',
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
      row['case-number'] = caseJSON['case_number'];
      row['judge'] = caseJSON['judge'];
      row['defense-attorney'] = caseJSON['defense_attorney'];
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
        actions={[
            {
                icon: 'assignment',
                tooltip: 'Update Case',
                onClick: (event, rowData) => {
                  console.log(rowData);
                  let case_number = rowData['case-number'];
                  window.location.href = `update/${case_number}`;
                },
            },
            {
                icon: 'date_range',
                tooltip: 'Enter Scheduling Order',
                // disabled: TODO Disable if trial is set ,
                onClick: (event, rowData) => {
                  if (rowData['trial'] !== undefined) {
                    alert("Scheduling order has already been entered for this case.")
                  } else {
                    let case_number = rowData['case-number'];
                    window.location.href = `track/${case_number}`;
                  }
                },
            },
            {
                icon: 'gavel',
                tooltip: 'New Motion',
                // disabled: TODO Disable if trial is not set ,
                onClick: (event, rowData) => {
                  if (rowData['trial'] === undefined) {
                    alert("No scheduling order has been entered for this case.")
                  } else {
                    let case_number = rowData['case-number'];
                    window.location.href = `motion/${case_number}`;
                  }
                },
            },
        ]}
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
              Save?
      </div>
        }}]}
      />
    )
  }
}

export default App;
