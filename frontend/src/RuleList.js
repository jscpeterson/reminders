import React from 'react'
import TextField, {HelperText, Input} from '@material/react-text-field';
import MaterialIcon from '@material/react-material-icon';
import MaterialTable from 'material-table'
import Cookies from 'js-cookie'

const DEADLINE_ACTIVE = "active";
const DEADLINE_COMPLETE = "complete";
const DEADLINE_EXPIRED = "expired";

class RuleList extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      management: this.props.management,
      columns: [
        { title: 'Defendant',
          field: 'defendant',
          editable: 'never' },
        { title: 'DA Case #',
          field: 'case-number',
          editable: 'never' },
        { title: 'CR #',
          field: 'cr-number',
          editable: 'never', },
        { title: 'Judge',
          field: 'judge' ,
          editable: 'never'},
        { title: 'Defense',
          field: 'defense-attorney' ,
          editable: 'never' },

        { title: 'Initial Witness List',
          field: 'initial-witness-list',
          type:'date',
          render: rowData => <span>{this.displayDate(rowData,'initial-witness-list')}</span>,
          editable: 'never' },
        { title: 'Scheduling Conference',
          field: 'scheduling-conference',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData,'scheduling-conference')}</span>,
          editable: 'never'
        },
        { title: 'PTIs Requested',
          field: 'ptis-requested',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData,'ptis-requested')}</span>,
          editable: 'never' },
        { title: 'PTIs Conducted',
          field: 'ptis-conducted',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData,'ptis-conducted', )}</span>,
          editable: 'never' },
        { title: 'Witness PTIs',
          field: 'witness-ptis',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData,'witness-ptis')}</span>,
          editable: 'never' },
        { title: 'Scientific Evidence',
          field: 'scientific-evidence',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData,'scientific-evidence')}</span>,
          editable: 'never' },
        { title: 'Pretrial Motion Filing',
          field: 'pretrial-motion-filing',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData,'pretrial-motion-filing')}</span>,
          editable: 'never' },

        { title: 'Final Witness List',
          field: 'final-witness-list',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData,'final-witness-list')}</span>,
          editable: 'never' },
        { title: 'Need for Interpreter',
          field: 'need-for-interpreter',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData,'need-for-interpreter',)}</span>,
          editable: 'never' },
        { title: 'Plea Agreement',
          field: 'plea-agreement',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData,'plea-agreement')}</span>,
          editable: 'never' },
        { title: 'Certification of Readiness',
          field: 'certification-of-readiness',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData,'certification-of-readiness')}</span>,
          editable: 'never' },
        { title: 'PTC/Docket Call',
          field: 'ptc/docket-call',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData,'ptc/docket-call')}</span>,
          editable: 'never' },
        { title: 'Trial',
          field: 'trial',
          type: 'date',
          render: rowData => <span>{this.displayDate(rowData,'trial')}</span>,
          editable: 'never' },

        {
          title: 'Stayed Case - YOU SHOULDN\'T SEE THIS',
          field: 'stayed',
          hidden: 'true,'
        }
      ],
      tableData: [],
      jsonData: []
    }
  }

  displayDate(rowData, key) {
    /** 
     * Displays a date as M/D/YYYY.
     * @param rowData: all of the case data from a given row
     * @param key: the key of the date to be displayed
     * @return {span} date with proper style and format
     */
    let date = rowData[key];
    let deadlineData = this.getDeadlineData(rowData, key);

    if (date) {
      let realDate = this.toDate(date);
      let dateString = this.formatDate(realDate);
      let deadlineUrgency = this.getDateUrgency(realDate, deadlineData, rowData);
      let bgColor = this.getDateBgColor(deadlineUrgency);
      const spanStyle = {
        backgroundColor: bgColor
      };
      const display = <span style={spanStyle}>{dateString}</span>;
      return display;
    } else {
      return <span></span>;
    }
  }

  getDeadlineData(rowData, key) {
      /**
       * Returns the json data for a deadline given the rowData for the case and the key corresponding to the deadline.
       * @param rowData: all of the case data from a given row
       * @param key: the key of the date to be displayed
       * @return json data for the deadline
       */
      let index = rowData['tableData'].id;
      let json = this.state.jsonData[index];
      let deadlines = json['deadline_set'];
      return deadlines.filter(function(data){ return data.type === key })[0];
  }

  getDateUrgency(dueDate, deadlineData, rowData) {
    /**
     * Returns urgency of deadline based on proximity to due date
     * @param {Date} dueDate Due date of deadline
     * @param deadlineData: json data for a deadline
     * @param rowData: data associated with the deadline's row
     * @return {string} urgency of deadline
     */
    const today = new Date();
    const daysLeft = daysBetween(today, dueDate);

    // Threshold days are one day before the reminders are sent out
    const thresholdInTroubleDays = deadlineData['first_reminder_days'] + 1;
    const thresholdUrgentDays = deadlineData['second_reminder_days'] + 1;

    if (rowData['stayed']) {
      return "Stayed";
    }

    else if (deadlineData['status'] === DEADLINE_COMPLETE){
      return "Completed";
    }

    else if (deadlineData['status'] === DEADLINE_EXPIRED) {
      return "Expired";
    }

    else if (deadlineData['status'] === DEADLINE_ACTIVE) {
      if (thresholdInTroubleDays < daysLeft) {
        return "OnTrack";
      } else if (thresholdUrgentDays < daysLeft && daysLeft <= thresholdInTroubleDays) {
        return "InTrouble";
      } else if (daysLeft <= thresholdUrgentDays) {
        return "Urgent";
      } else {
        return "Default";
      }
    }

    else {
      // Status is incorrect if code hits this point
      return "Default";
    }

  }

  getDateBgColor(urgency) {
    /**
     * Returns background color for date cell based on due date
     * @param {string} urgency Indicates how close a deadline is to due date
     * @return {string} background color to use for date
     */
    return bgColors[urgency];
  }

  toDate(date) {
    /**
     * Accepts date as string or date and returns to date
     * @param date Date as string or Date
     * @return {Date} date
     */
    if (typeof(date) === 'string') {
      return new Date(date);
    } else {
      return date;
    }
  }

  formatDate(date) {
    /**
     * Formats the date as M/D/YYYY
     * @param {Date} date
     * @return {string} properly formatted date string
     */    
    
     // Could use Moment.js here instead...
    const day = date.getDate().toString();
    const month = (date.getMonth() + 1).toString();
    const year = date.getFullYear().toString();

    return month.concat('/', day, '/', year)
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
      row['cr-number'] = caseJSON['cr_number'];
      row['judge'] = caseJSON['judge'];
      row['defense-attorney'] = caseJSON['defense_attorney'];
      row['notes'] = caseJSON['notes'];
      row['stayed'] = caseJSON['stayed'];

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
    let url = "/api/cases";
    if (this.state.management) {
        url = "/api/staff_cases";
    }

    return fetch(url)
      .then(response => response.json())
      .then(cases => this.populateTable(cases))
  }

  putData(data) {
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
                  let case_number = rowData['case-number'];
                  window.location.href = `update/${case_number}`;
                },
            },
            {
                icon: 'date_range',
                tooltip: 'Enter Scheduling Order',
                // disabled: TODO Disable if trial is set ,
                onClick: (event, rowData) => {
                  if (rowData['stayed']) {
                    alert('Case is stayed')
                  } else {
                    if (rowData['trial'] !== undefined) {
                      alert("Scheduling order has already been entered for this case.")
                    } else {
                      let case_number = rowData['case-number'];
                      window.location.href = `track/${case_number}`;
                    }
                  }
                },
            },
            {
                icon: 'gavel',
                tooltip: 'New Motion',
                // disabled: TODO Disable if trial is not set ,
                onClick: (event, rowData) => {
                  if (rowData['stayed']) {
                    alert('Case is stayed')
                  } else {
                    if (rowData['trial'] === undefined) {
                      alert("No scheduling order has been entered for this case.")
                    } else {
                      let case_number = rowData['case-number'];
                      window.location.href = `motion/${case_number}`;
                    }
                  }
                },
            },
            {
                icon: 'pan_tool',
                tooltip: 'Stay/Resume Case',
                onClick: (event, rowData) => {
                  let case_number = rowData['case-number'];
                  if (!rowData['stayed']) {
                    window.location.href = `stay_case/${case_number}`;
                  } else {
                    window.location.href = `resume_case/${case_number}`;
                  }
                }
            },
            {
                icon: 'event_available',
                tooltip: 'Close Case',
                onClick: (event, rowData) => {
                  if (confirm("This will end all deadlines and close the case. You will not be able to reopen it. " +
                      "Are you sure?")) { // Consider moving confirmation to its own URL so it's more noticeable.
                    let case_number = rowData['case-number'];
                    window.location.href = `case_closed/${case_number}`;
                  }
                }
            },
            // {
            //     icon: 'bug_report',
            //     tooltip: 'Debug',
            //     onClick: (event, rowData) => {
            //       console.log(rowData);
            //       console.log(this.state.tableData);
            //       console.log(this.state.jsonData);
            //     }
            // },
        ]}
        detailPanel={[{
            tooltip: 'Notes',
            render:rowData => {
            return <div>
        <TextField
          // helperText={<HelperText>Save</HelperText>}
          onTrailingIconSelect={() => {this.putNotes(rowData)}}
          trailingIcon={<MaterialIcon aria-label="Save" role="button" icon="check" hasRipple={true}/>}
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

const bgColors = {
  "Stayed": "#C0C0C0", // light gray
  "Expired": "#808080", // dark gray
  "Completed": "#66B2FF", // light blue
  "OnTrack": "#66FF66", // light green
  "InTrouble": "#FFFF66", // light yellow
  "Urgent": "#FF6666", // light red
  "Default": "#FFFFFF" // white
} 

// Per this source
// https://stackoverflow.com/questions/542938/how-do-i-get-the-number-of-days-between-two-dates-in-javascript
function treatAsUTC(date) {
  /**
   * Converts date to UTC
   * @param {Date} date Date in any timezone
   * @return {Date} Date as UTC
   */
    let result = new Date(date);
    result.setMinutes(result.getMinutes() - result.getTimezoneOffset());
    return result;
}

function daysBetween(startDate, endDate) {
  /**
   * Finds days between two dates
   * @param {Date} startDate Start date
   * @param {Date} endDate End date
   * @return {number} Date as UTC
   */
    const millisecondsPerDay = 24 * 60 * 60 * 1000;
    return (treatAsUTC(endDate) - treatAsUTC(startDate)) / millisecondsPerDay;
}

export default RuleList;