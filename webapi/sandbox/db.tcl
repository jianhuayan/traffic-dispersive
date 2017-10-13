############################################################################
# Copyright 2014 Aurora Networks
# db.tcl Driver to connect and query the database
# A driver for initializing. interacting with, and destroying a communications
# session with the MySQL database.
############################################################################
namespace eval db {
    variable initialized   0
    variable mysql_handle
    array set valid_var_names {}
    # variable database_name automation
    variable database_name AssetPrice 
}

############################################################################
# Login to MySQL and connect to $db::database_name, creating db::mysql_handle.
############################################################################
proc db::init {} {
    if {$db::initialized == 1} {
	return
    }
    set port 3306
    set host localhost
    set user mysql
    set password mysql
    test::log "connecting to MySQL..."
    set db::mysql_handle [mysqlconnect -host $host -port $port -user $user -password $password]
    mysqluse $db::mysql_handle $db::database_name

    # Debugging info:
    # Useful command is "mysqlinfo handle option"
    # Return various database information depending on the option. The option must be one of the following keywords.

    # Return a String with information about last operation. "Records: 3 Duplicates: 0 Warnings: 0" by INSERT or "Rows 
    # matched: 40 Changed: 40 Warnings: 0" by UPDATE statements (read the manual for mysql_info in mysql C API documentation)
    # test::log "Last operation info: [mysqlinfo $db::mysql_handle info]"
    
    # Return a list of all database names known to the server. The handle must be connected.
    # test::log "All database names known to server: [mysqlinfo $db::mysql_handle databases]"
    
    # Return the name of the database with which the handle is associated. The handle must be in use.
    # test::log "Name of database with which handle is associated: [mysqlinfo $db::mysql_handle dbname]"
    
    # Return the name of the host to which the handle is connected. The handle must be connected.
    # test::log "Name of the host with which handle is connected: [mysqlinfo $db::mysql_handle host]"
    
    # Return a list of all table names in the database with which the handle is associated. The handle must be in use.
    # test::log "List of all table names in database with which handle is associated: [mysqlinfo $db::mysql_handle tables]"
    
    set table_list [mysqlinfo $db::mysql_handle tables]
    foreach table $table_list {
	test::log "Table: $table"
	catch {db::get_column_names $table} column_list
	test::log "column_list=$column_list"
	foreach column $column_list {
	    set column [lindex $column 0]
	    lappend db::valid_var_names($table) $column
	    if {![info exists db::valid_var_names($column)]} {
		set db::valid_var_names($column) $table
	    } else {
		lappend db::valid_var_names($column) $table
	    }
	}
    }
    set db::initialized 1
}

############################################################################
# Return all column names in $table
############################################################################
proc db::get_column_names {table} {
    return [mysqlcol $db::mysql_handle $table name]
}

############################################################################
# PUBLIC proc to get a single value from a column in a table, based on a key
# Use -distinct to eliminate redundant data.
############################################################################
proc db::query {table column key value args} {
    set distinct ""
    while { [llength $args] } {
        switch -- [lindex $args 0] {
            -distinct {
                set distinct "DISTINCT"
                set args [lrange $args 1 end]
            }
            default {
                error "Invalid args:[lindex $args 0] passed to [info level 0]."
            }
        }
    }
    set unesc_query "SELECT $distinct $column FROM $table WHERE $key = \'$value\'"
    set query [mysqlescape $unesc_query]
    set command "mysqlsel $db::mysql_handle \"$query\" -flatlist"
    set result [eval $command]
    return $result
}

############################################################################
# PUBLIC proc to get an entire row from a table, based on a key
############################################################################
proc db::query_row {table key value} {
    set unesc_query "SELECT * FROM $table WHERE $key = \'$value\'"
    set query [mysqlescape $unesc_query]
    set command "mysqlsel $db::mysql_handle \"$query\" -flatlist"
    set result [eval $command]
    return $result
}

############################################################################
# PUBLIC proc to get an entire column from a table.
# Use -distinct to eliminate redundant data.
############################################################################
proc db::query_column {table column args} {
    set distinct ""
    while { [llength $args] } {
        switch -- [lindex $args 0] {
            -distinct {
                set distinct "DISTINCT"
                set args [lrange $args 1 end]
            }
            default {
                error "Invalid args:[lindex $args 0] passed to [info level 0]."
            }
        }
    }
    set unesc_query "SELECT $distinct $column FROM $table"
    set query [mysqlescape $unesc_query]
    set command "mysqlsel $db::mysql_handle \"$query\" -flatlist"
    set result [eval $command]
    return $result
}

############################################################################
# PUBLIC proc to insert a row into a table. Use with care!
# col_list is a list of columns
# val_list is a list of values
############################################################################
proc db::insert {table col_list val_list} {
    # set statement "INSERT INTO $table \($col_list\) VALUES \($val_list\)"
    set statement "INSERT INTO `$table` VALUES ($val_list)"
    set command "mysqlexec $db::mysql_handle \"$statement\""
    test::log "command=$command"
    set result [eval $command]
    return $result
}

############################################################################
# Manpage of mysqltcl, whole thing just if 0'd out.
############################################################################
proc db::manpage {} {
if 0 {

MySQLTcl

 
NAME

MySQLTcl - MySQL server access commands for Tcl  
INTRODUCTION

MySQLTcl is a collection of Tcl commands and a Tcl global array that provide access to one or more mysql database servers. MySQLTcl is nothing more than a patched version of a patched version of Hakan Soderstrom's patch of Tom Poindexter's Sybtcl. Most of the documentention has been left as it was when I started to work with this interface (a patch of msqltcl-1.50). However, I have tried to replace appropriate occurrences of msql by MySQL. I have changed the semantics of two commands: mysqlconnect and mysqlcol. Everything else should work as before. The new versions are described below.
 

MYSQLTCL COMMANDS

mysqlconnect ?option value ...?

Connect to a mysql server. A handle is returned which should be used in all other mysqltcl commands using this connection. mysqlconnect raises a Tcl error if the connection fails. mysqlconnect read first the options from my.cnf file group mysqltcl. See mysql documentation chapter "options files". Possible connection options are:
-host hostname

The host on which the server is located. The local host is used by default.
-user user

The user whose name is used for the connection. The current Unix username is used by default.
-password password

The password that must be used for the connection. If it is not present, the connection is possible only for users with no password on the server.
-db db

If this option is present, db is used as current database, with no need for a call to mysqluse.
-port port

The port number for the TCP/IP connection, if it's different from the default.
-socket socket

The socket or named pipe for the connection.
mysqluse handle dbname

Associate a connected handle with a particular database. If successful the handle is said to be in use. Handle must be a valid handle previously obtained from mysqlconnect.
Mysqluse raises a Tcl error if the handle is not connected or if the database name specified could not be used.

mysqlsel handle sql-statement ?-list|-flatlist?

Send sql-statement to the server. The handle must be in use (through mysqlconnect and mysqluse).
If sql-statement is a SELECT statement and no -list or -flatlist option is specified, the command returns the number of rows returned as the result of the query. The rows can be obtained by the mysqlnext and/or the mysqlmap commands. The resulting rows are called the pending result.

If sql-statement is a SELECT statement and -list or -flatlist is specified, the command returns the full list of rows returned as the result of the query in one of two possible formats:

[1]
-list generates a list of lists, in which each element is a row of the result.
[2]
-flatlist generates the concatenation of all rows in a single list, which is useful for scanning with a single foreach.
An example is in order: 
       % mysqlsel $db "SELECT ID, NAME FROM FRIENDS" -list

{1 Joe} {2 Phil} {3 John}

       % mysqlsel $db "SELECT ID, NAME FROM FRIENDS" -flatlist

{1 Joe 2 Phil 3 John}

Note that both list syntaxes are faster than something like 

    % mysqlsel $db "SELECT ID, NAME FROM FRIENDS" 

    3 

% mysqlmap $db {id name} {lappend result $id $name} 

    % puts $result 
{1 Joe 2 Phil 3 John}

If sql-statement is a valid mysql statement, but not a SELECT statement, the command returns -1 after executing the statement, or an empty string if -list or -flatlist is specified. There is no pending result in this case.

In any case mysqlsel implicitly cancels any previous result still pending for the handle.

mysqlexec handle sql-statement

Send sql-statement, a mysql non-SELECT statement, to the server. The handle must be in use (through mysqlconnect and mysqluse).
Mysqlexec implicitly cancels any previous result pending for the handle.

If sql-statement is a valid mysql SELECT statement, the statement is executed, but the result is discarded. No Tcl error is generated. This amounts to a (potentially costly) no-op. Use the mysqlsel command for SELECT statements.

mysqlexec return the number of affected rows (DELETE, UPDATE)

mysqlquery handle sql-select-statement

Send sql-select-statement to the server. New command in 2.1 version.
mysqlquery allow to send multiple nested queries on one handle (without need to build new handle or caching results). mysqlquery return a query handle that can be used as handle in commands as (mysqlnext, mysqlmap, mysqlseek, mysqlcol, mysqlresult). After result proceeding all query must be freed with mysqlendquery query-hanlde command.

An example is in order: 
set query1 [mysqlquery $db {SELECT ID, NAME FROM FRIENDS}]

while {[set row [mysqlnext $query1]]!=""} {

    set id [lindex $row 0]

    set query2 [mysqlquery $db "SELECT ADDRESS FROM ADDRESS WHERE FRIENDID=$ID"]

    mysqlmap $query2 address { puts "address = $address }

               mysqlendquery $query2

       }

       mysqlendquery $query1


mysqlendquery query-handle

free result memory after mysqlquery command. New command in 2.1 version. You must invoke mysqlendquery after each mysqlquery to not cause memory leaks. See mysqlquery command.
Using mysqlendquery on db-handle will free also memory after mysqlsel command.

mysqlnext handle
(note: In most cases one should use sql-joins and avoid nested queries. SQL-sever can optimize such queries. But in some applications (GUI-Forms) where the results are used long time the inner query is not known before)

Mysqlnext raises a Tcl error if there is no pending result for handle.

mysqlmap handle binding-list script

Iterate a script over the rows of the pending result. Mysqlmap may consume all rows or only some of the rows of the pending result. Any remaining rows may be obtained by further mysqlnext or mysqlmap commands.
Handle must be a handle with a pending result from a previous mysqlsel command. Binding-list must be a list of one or more variable names. Script must be a Tcl script. It may be empty, but usually it contains one or more commands.

Mysqlmap processes one row at a time from the pending result. For each row the column values are bound to the variables in the binding list, then the script is executed. Binding is strictly positional. The first variable in the binding list is bound to the first column of the row, and so on. The variables are created in the current context (if they do not already exist). A variable name beginning with a hyphen is not bound; it serves as a placeholder in the binding list. If there are more columns than variables the extra columns are ignored.

The mysqlmap command is similar to an ordinary foreach. A foreach iterates over the elements of a list, mysqlmap iterates over the rows of a pending result. In both cases iteration is affected by break and continue Tcl commands. The binding list variables retain their last values after the command has completed.

A simple example follows. Assume $db is a handle in use.

mysqlsel $db {select lname, fname, area, phone from friends

    order by lname, fname}

mysqlmap $db {ln fn - phone} {

    if {$phone == {}} continue

    puts [format "%16s %-8s %s" $ln $fn $phone]

}

The mysqlsel command gets and sorts all rows from table friends. The mysqlmap command is used to format and print the result in a way suitable for a phone list. For demonstration purposes one of the columns (area) is not used. The script begins by skipping over rows which have no phone number. The second command in the script formats and prints values from the row.

Mysqlmap raises a Tcl error if there is no pending result for handle, or if binding-list contains more variables than there are columns in the pending result.

mysqlseek handle row-index

Moves the current position among the rows in the pending result. This may cause mysqlnext and mysqlmap to re-read rows, or to skip over rows.
Row index 0 is the position just before the first row in the pending result; row index 1 is the position just before the second row, and so on. You may specify a negative row index. Row index -1 is the position just before the last row; row index -2 is the position just before the second last row, and so on. An out-of-bounds row index will cause mysqlseek to set the new current position either just before the first row (if the index is too negative), or just after the last row (if the index exceeds the number of rows). This is not an error condition.

Mysqlseek returns the number of rows that can be read sequentially from the new current position. Mysqlseek raises a Tcl error if there is no pending result for handle.

Portability note: The functionality of mysqlseek is frequently absent in other Tcl extensions for SQL.

mysqlcol handle table-name option
mysqlcol handle table-name option-list
mysqlcol handle table-name option ?option ...?

Return information about the columns of a table. Handle must be in use. Table-name must be the name of a table; it may be a table name or -current if there is a pending result. One or more options control what information to return. Each option must be one of the following keywords.
name

Return the name of a column.
type

Return the type of a column; one of the strings decimal, tiny, short, long, float, double, null, timestamp, long long, int24, date, time, date time, year, new date, enum, set, tiny blob, medium blob, long blob, blob, var string, or string. Note that a column of type char will return tiny, while they are represented equally.
length

Return the length of a column in bytes.
table

Return the name of the table in which this column occurs.
non_null

Return the string ``1'' if the column is non-null; otherwise ``0''.
prim_key

Return the string ``1'' if the column is part of the primary key; otherwise ``0''.
numeric

Return the string ``1'' if the column is numeric; otherwise ``0''.
decimals

Return the string ``1'' if the column is non-null; otherwise ``0''.
The three forms of this command generate their result in a particular way.

[1]
If a single option is present the result is a simple list of values; one for each column.
[2]
If the options are given in the form of an option list the result is a list of lists. Each sublist corresponds to a column and contains the information specified by the options.
[3]
If several options are given, but not in a list, the result is also a list of lists. In this case each sublist corresponds to an option and contains one value for each column.
The following is a sample interactive session containing all forms of the mysqlcol command and their results. The last command uses the -current option. It could alternatively specify the table name explicitly.

       % mysqlcol $db friends name

       fname lname area phone

% mysqlcol $db friends {name type length}

{fname char 12} {lname char 20} {area char 5} {phone char 12}

% mysqlsel $db {select * from friends}

       % mysqlcol $db -current name type length

{fname lname area phone} {char char char char} {12 20 5 12}
mysqlinfo handle option

Return various database information depending on the option. The option must be one of the following keywords.
info

Return a String with information about last operation. "Records: 3 Duplicates: 0 Warnings: 0" by INSERT or "Rows matched: 40 Changed: 40 Warnings: 0" by UPDATE statements (read the manual for mysql_info in mysql C API documentation)
databases

Return a list of all database names known to the server. The handle must be connected.
dbname

Return the name of the database with which the handle is associated. The handle must be in use.
dbname?

Return the name of the database with which the handle is associated; an empty string if the handle is connected, but not in use.
host

Return the name of the host to which the handle is connected. The handle must be connected.
host?

Return the name of the host to which the handle is connected; an empty string if the handle is not connected.
tables

Return a list of all table names in the database with which the handle is associated. The handle must be in use.
mysqlresult handle option

Return information about the pending result. Note that a result is pending until canceled by a mysqlexec command, even if no rows remain to be read. Option must be one of the following keywords.
cols

Return the number of columns in the pending result. There must be a pending result.
cols?

Return the number of columns in the pending result; an empty string if no result is pending.
current

Return the current position in the pending result; a non-negative integer. This value can be used as row-index in the mysqlseek command. An error is raised if there is no pending result.
current?

As above, but returns an empty string if there is no pending result.
rows

Return the number of rows that can be read sequentially from the current position in the pending result. There must be a pending result.
rows?

Return the number of rows that can be read sequentially from the current position in the pending result; an empty string if no result is pending.
*
Note that [mysqlresult $db current] + [mysqlresult $db rows] always equals the total number of rows in the pending result.
mysqlstate handle ?-numeric?

Return the state of a handle as a string or in numeric form. There is no requirement on handle; it may be any string. The return value is one of the following strings, or the corresponding numeric value if -numeric is specified. The states form a progression where each state builds on the previous.
NOT_A_HANDLE (0)

The string supplied for handle is not a mysqltcl handle at all.
UNCONNECTED (1)

The string supplied for handle is one of the possible mysqltcl handles, but it is not connected to any server.
CONNECTED (2)

The handle is connected to a server, but not associated with a database.
IN_USE (3)

The handle is connected and associated with a database, but there is no pending result.
RESULT_PENDING (4)

The handle is connected, associated with a database, and there is a pending result.
mysqlclose ?handle?

Closes the server connection associated with handle, causing it to go back to the unconnected state. Closes all connections if handle is omitted. Returns an empty string. Mysqlclose raises a Tcl error if a handle is specified which is not connected.
mysqlinsertid handle

Returns the auto increment id of the last INSERT statement.
mysqlescape string

Returns the content of string, with all special characters escaped, so that it is suitable for use in an SQL statement. This is simpler (faster) than using a general regexp.
 
STATUS INFORMATION

Mysqltcl creates and maintains a Tcl global array to provide status information. Its name is mysqlstatus. Mysqlstatus elements:
code

A numeric conflict code set after every mysqltcl command. Zero means no conflict; non-zero means some kind of conflict. All conflicts also generate a Tcl error.
All mysql server conflicts set mysqlstatus(code) to the numeric code of the mysql error. 
Any other conflict sets mysqlstatus(code) to -1.

command

The last failing mysqltcl command. Not updated for successful commands.
message

Message string for the last conflict detected. The same string is returned as the result of the failing mysqltcl command. Not updated for successful commands.
nullvalue

The string to use in query results to represent the SQL null value. The empty string is used initially. You may set it to another value.
 
ENVIRONMENT VARIABLES

None.
 

BUGS & POSSIBLE MISFEATURES

Sure. Some of the options of the information commands (mysqlinfo, mysqlresult, mysqlcol, mysqlstate) keep returning results even if the mysql server has ceased to exist. Deleting any of the mysqltcl commands closes all connections.
 

AUTHORS

Tobias Ritzau (tobri@ida.liu.se) 
Paolo Brutti (Paolo.Brutti@tlsoft.it) 
Artur Trzewik (mail@xdobry.de) 
MySQLTcl is derived from a patch of msql by Hakan Soderstrom (hs@soderstrom.se), Soderstrom Programvaruverkstad, S-12242 Enskede, Sweden. msql is derived from Sybtcl by Tom Poindexter (tpoindex@nyx.cs.du.edu).
$Revision: 1.1.1.1 $

 
Index

NAME
INTRODUCTION
MYSQLTCL COMMANDS
STATUS INFORMATION
ENVIRONMENT VARIABLES
BUGS & POSSIBLE MISFEATURES
AUTHORS
This document was created by man2html, using the manual pages.
Time: 19:56:25 GMT, December 04, 2002
}
}
