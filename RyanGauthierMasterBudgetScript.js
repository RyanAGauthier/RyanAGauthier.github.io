if(1){
function nameSheets(){
var sheets = SpreadsheetApp.getActiveSpreadsheet().getSheets();
if (sheets.length > 1) {
  for(var temp = 0; temp < sheets.length; temp++)
  {
  Logger.log(sheets[temp].getName());
  }
}
}
var PODate = 1 - 1;
var EmailAdd = 2 - 1;
var TeamName = 3 - 1;
var ExpectCost = 15 - 1;
var ApprovedColumn = 16 - 1;
var Comments = 17 - 1;
var TotalCost = 18 - 1;
var PaidFor = 19 - 1;
var EmailLog = 22 - 1;
var ColumnMech = 2;
var ColumnCont = 12;
var ColumnElec = 22;
var ColumnBusi = 30;
function onEdite(e) {
  /*Any weird off by one things are probably because rows are counted starting from 1, but the array they're stored in starts from 0
  In addition, this function is called ANY time a cell is edited, so ideally you write the comment first, then change the "approved" stuff to yes or no 
  Until I can figure out how to start from the last spot without an approved thing, this will do*/
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet().getSheets();
  var sheet;
  var budget;
  if(spreadsheet[0].getName() == "Form Responses 3")
  {
    sheet = spreadsheet[0];
    budget = spreadsheet[1];
    //Logger.log("Successfully identified Form Responses 3");
  }
  else
  {
     sheet = spreadsheet[1];
    //Logger.log("Successfully identified Form Responses 3");
     budget = spreadsheet[0];
  }
  //var d = new Date();
  //var currentRow = 2;
  var dataRange;
  var valueMatrix;
  var tempString1 = '';
  var tempString2 = '';
  var tempString3 = '';
  var numActiveColumns = sheet.getLastColumn(); 
  var numActiveColumnsB = budget.getLastColumn();
  var numActiveRows = sheet.getLastRow();
  var numActiveRowsB = budget.getLastRow();
  var valueMatrixB;
  var dataRangeB;
  //var dataRange = sheet.getRange(2, 1, numActiveRows, numActiveColumns);
  //var valueMatrix = dataRange.getValues();//this gets all the values in the entire sheet into a temporary matrix, might take a long time with more responses
  for(var temp = 0; temp < (numActiveRows - 1); temp++)
  {
    dataRange = sheet.getRange(temp + 2, 1, 1, numActiveColumns);// gets the current row in the loop
    valueMatrix = dataRange.getValues();
    dataRangeB = budget.getRange(1, 1, numActiveRowsB + 1, numActiveColumnsB + 1);// gets the entire budget spreadsheet
    //valueMatrixB = dataRangeB.getValues();
    Logger.log(valueMatrix);
    Logger.log(valueMatrix[0][EmailLog]);
    if((valueMatrix[0][PaidFor] == "Y" || valueMatrix[0][PaidFor] == "y"))//need to check if item was already logged in second spreadsheet, if not, add it to budget
    {
      Logger.log("Trying to change master budget sheet!");
      var relevantColu;
      if(valueMatrix[0][TeamName] == "Mechanical")
      {
        relevantColu = ColumnMech;
      }
      else if(valueMatrix[0][TeamName] == "Controls")
      {
        relevantColu = ColumnCont;
      }
      else if(valueMatrix[0][TeamName] == "Electrical")
      {
        relevantColu = ColumnElec;
      }
      else if(valueMatrix[0][TeamName] == "Business")
      {
        relevantColu = ColumnBusi;
      };
      for(var tempo = 0; tempo < (numActiveRowsB - 1); tempo++)
      {
        var cell = dataRangeB.getCell(tempo + 5, relevantColu);
           if(cell.isBlank())
           {
             Logger.log("Trying to set values in budget directly");
            cell.setValue(parseFloat(valueMatrix[0][TotalCost]));
            cell = dataRangeB.getCell(tempo + 5, relevantColu + 1);
            cell.setValue(valueMatrix[0][PODate]);
             SpreadsheetApp.flush();
             break;
           }
        else
        {
          cell = dataRangeB.getCell(tempo + 5, relevantColu + 1);//checking dates to see if its a repeat submission
         /* Logger.log("Incoming getValue of Date");
          Logger.log(cell.getValue());
          Logger.log("Incoming comparison value");
          Logger.log(valueMatrix[0][PODate]);
          Logger.log(cell.getValue() - valueMatrix[0][PODate]);*/
          if((cell.getValue() - valueMatrix[0][PODate]) == 0) //for some reason these two values just sum up to 0, but aren't exactly the same
          {
            Logger.log("Repeat Date found!");
            break;
          }
        }
      }
   
      //var Avals = budget.getRange("A1:A").getValues();//javascript magic for determining last 
      //var Alast = Avals.filter(String).length;//row without a value if all cells preceding are filled
      
    }
    if((valueMatrix[0][ApprovedColumn] == "Y" || valueMatrix[0][ApprovedColumn] == "y")&&((valueMatrix[0][EmailLog] == "")))
    {
      Logger.log("I entered the loop!");
      tempString1 = valueMatrix[0][EmailAdd];
      tempString2 = valueMatrix[0][Comments];
      tempString3 = valueMatrix[0][PODate];
      Logger.log(tempString1 + ' ' + tempString2 + tempString3);
      var relevantColu;
      if(valueMatrix[0][TeamName] == "Mechanical")
      {
        relevantColu = ColumnMech;
      }
      else if(valueMatrix[0][TeamName] == "Controls")
      {
        relevantColu = ColumnCont;
      }
      else if(valueMatrix[0][TeamName] == "Electrical")
      {
        relevantColu = ColumnElec;
      }
      else if(valueMatrix[0][TeamName] == "Business")
      {
        relevantColu = ColumnBusi;
      };
      var percentLeft = dataRangeB.getCell(4, relevantColu);// gets the current expenditure percentage
      if(valueMatrix[0][PaidFor] == "Y" || valueMatrix[0][PaidFor] == "y")
      {
      MailApp.sendEmail(tempString1, 'Your Purchase Order Has Been Approved','Your purchase order placed on ' + tempString3 + ' was approved.\n'
                        + 'The ' + valueMatrix[0][TeamName] + ' Team has utilized ' + percentLeft.getValue().toFixed(2)
      + '% of its budget.\n' + 'Additional comments: ' + tempString2); 
      }
      else
      {
        var adjustmentNum = dataRangeB.getCell(3, relevantColu).getValue();
        var adjustmentDen = dataRangeB.getCell(2, relevantColu).getValue();
      MailApp.sendEmail(tempString1, 'Your Purchase Order Has Been Approved','Your purchase order placed on ' + tempString3 + ' was approved.\n'
                        + 'The ' + valueMatrix[0][TeamName] + ' Team has utilized ' + ((adjustmentNum + valueMatrix[0][ExpectCost])/adjustmentDen).toFixed(2)
      + '% of its budget.\n' + 'Additional comments: ' + tempString2); 
      }
      dataRange = sheet.getRange(temp + 2, EmailLog + 1);
      dataRange.setValue("Sent");
      Logger.log("I set a value :" + dataRange.getValue());
    }
    else if((valueMatrix[0][ApprovedColumn] == "N" || valueMatrix[0][ApprovedColumn] == "n")&&(valueMatrix[0][EmailLog] == ""))
    {
      MailApp.sendEmail(valueMatrix[0][EmailAdd], "Your Purchase Order Has Been Denied", valueMatrix[0][Comments]); 
      dataRange = sheet.getRange(temp + 2, EmailLog + 1);
      dataRange.setValue("Sent");
    }
    SpreadsheetApp.flush();
  } 
}
}