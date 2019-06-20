import React, { Component } from 'react'
import ReactDOM from 'react-dom'
import MaterialTable from 'material-table'

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      columns: [
        { title: 'Defendant', field: 'defendant', editable: 'never' },
        { title: 'CR#', field: 'case_number', editable: 'never' },
        { title: 'Judge', field: 'judge' , editable: 'onUpdate'},
        { title: 'Defense', field: 'defense' , editable: 'onUpdate' },

        { title: 'Notes', field: 'notes', editable: 'onUpdate' },

          // TODO Change the names of these fields
        { title: 'Witness List', field: '1', type: 'date', editable: 'never' },
        { title: 'Scheduling Conference', field: '2', type: 'date', editable: 'never' },
        { title: 'Request PTIs', field: '3', type: 'date', editable: 'never' },
        { title: 'Conduct PTIs', field: '4', type: 'date', editable: 'never' },
        { title: 'Witness PTIs', field: '5', type: 'date', editable: 'never' },
        { title: 'Scientific Evidence', field: '6', type: 'date', editable: 'never' },
        { title: 'Pretrial Conference', field: '7', type: 'date', editable: 'never' },
        { title: 'Final Witness List', field: '8', type: 'date', editable: 'never' },
        { title: 'Need for Interpreter', field: '9', type: 'date', editable: 'never' },
        { title: 'Plea Agreement', field: '10', type: 'date', editable: 'never' },
        { title: 'Trial', field: '11', type: 'date', editable: 'never' },

      ],
      data: []
    }
  }

  populateJson(json) {
    let dataArray = [
        { defendant: 'Scruff McGruff', case_number: '2019-00000', judge: 'Judy', defense: 'Lionel Hutz',
          1: '2019/07/04', 2:'2019/07/04', 3: '2019/07/04', 4:'2019/07/04', 5:'2019/07/04', 6:'2019/07/04', 7:'2019/07/04' ,8: '2019/07/04',9: '2019/07/04',10:'2019/07/04', 11:'2019/07/04',
      },

      { defendant: 'Mitch Connor', case_number: '2019-00000', judge: 'Judy', defense: 'Lionel Hutz',
          1: '2019/07/04', 2:'2019/07/04', 3: '2019/07/04', 4:'2019/07/04', 5:'2019/07/04', 6:'2019/07/04', 7:'2019/07/04' ,8: '2019/07/04',9: '2019/07/04',10:'2019/07/04', 11:'2019/07/04',
      },

      { defendant: 'Scruff McGruff', case_number: '2019-00000', judge: 'Joe Brown', defense: 'Lionel Hutz',
          1: '2019/07/04', 2:'2019/07/04', 3: '2019/07/04', 4:'2019/07/04', 5:'2019/07/04', 6:'2019/07/04', 7:'2019/07/04' ,8: '2019/07/04',9: '2019/07/04',10:'2019/07/04', 11:'2019/07/04',
      },

      { defendant: 'Billy the Kid', case_number: '2019-00000', judge: 'Judy', defense: 'Lionel Hutz',
          1: '2019/07/04', 2:'2019/07/04', 3: '2019/07/04', 4:'2019/07/04', 5:'2019/07/04', 6:'2019/07/04', 7:'2019/07/04' ,8: '2019/07/04',9: '2019/07/04',10:'2019/07/04', 11:'2019/07/04',
      },

      { defendant: 'Scruff McGruff', case_number: '2019-00000', judge: 'Judy', defense: 'Lionel Hutz',
          1: '2019/07/04', 2:'2019/07/04', 3: '2019/07/04', 4:'2019/07/04', 5:'2019/07/04', 6:'2019/07/04', 7:'2019/07/04' ,8: '2019/07/04',9: '2019/07/04',10:'2019/07/04', 11:'2019/07/04',
      },
      {
        defendant: 'Hulk Hogan', case_number: '2019-00001', judge: 'Maury', defense: 'Saul Goodman',
        1: '2019/07/04', 2:'2019/07/04', 3: '2019/07/04', 4:'2019/07/04', 5:'2019/07/04', 6:'2019/07/04', 7:'2019/07/04' ,8: '2019/07/04',9: '2019/07/04',10:'2019/07/04', 11:'2019/07/04',
      }
     ]

    // dataArray = []

    json.forEach(function(x){
        // TODO Get deadlines for this case
        console.log(x); // TODO Append data to data array
    });

    this.setState(
        {data: dataArray}
    )
  }

  fetchJson() {
    return fetch("http://127.0.0.1:8000/api/cases/")
          .then(response => response.json())
          .then(json => this.populateJson(json))
  }

  componentDidMount() {
    this.fetchJson();
  }

  render() {
    return (
      <MaterialTable
        title="Rule List"
        columns={this.state.columns}
        data={this.state.data}
        // TODO Set default to 10 rows or infinite
          // TODO Remove trash can icon
          // TODO Remove ability to add rows
          // TODO Make notes field bigger
        editable={{
            isDeletable: rowData => null, // no rows should be deletable
          onRowAdd: newData =>
            new Promise((resolve, reject) => {
              setTimeout(() => {
                {
                  const data = this.state.data;
                  data.push(newData);
                  this.setState({ data }, () => resolve());
                }
                resolve()
              }, 1000)
            }),
          onRowUpdate: (newData, oldData) =>
              // TODO Updating the row should PATCH to case data
              new Promise((resolve, reject) => {
              setTimeout(() => {
                {
                  const data = this.state.data;
                  const index = data.indexOf(oldData);
                  data[index] = newData;
                  this.setState({ data }, () => resolve());
                }
                resolve()
              }, 1000)
            }),
          onRowDelete: oldData =>
            new Promise((resolve, reject) => {
              setTimeout(() => {
                {
                  let data = this.state.data;
                  const index = data.indexOf(oldData);
                  data.splice(index, 1);
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
