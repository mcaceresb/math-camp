* Email program
capture program drop mail_notify
program mail_notify
    syntax, rc(int) progname(str) stime(str) [attach(str) email(str) CAPture]
    if ( `"`email'"' == "" ) {
        local uname: env LOGNAME
        local email `uname'@nber.org
    }
    local etime "$S_TIME $S_DATE"
    local time  "Start: `stime'\nEnd: `etime'"
    if (`rc' == 0) {
        di "End: $S_TIME $S_DATE"
        local paux	  ran [Automated Message]
        local message = "`progname' finished running\n\n`time'"
        local subject = "`progname' `paux'"
    }
    else if ("`capture'" == "") {
        di "WARNING: $S_TIME $S_DATE"
        local paux ran with non-0 exit status [Automated Message]
        local message = "`progname' ran but Stata gave error code r(`rc')\n\n`time'"
        local subject = "`progname' `paux'"
    }
    else {
        di "ERROR: $S_TIME $S_DATE"
        local paux ran with errors [Automated Message]
        local message = "`progname' stopped with error code r(`rc')\n\n`time'"
        local subject = "`progname' `paux'"
    }
    di "`subject'"
    di "`message'"
    if ( "`attach'" != "" ) {
        shell echo -e "`message'" | mail -a "`attach'" -s "`subject'" `email'
    }
    else {
        shell echo -e "`message'" | mail -s "`subject'" `email'
    }
end

capture mata: mata drop save_table()
mata:
void function save_table(
    string scalar output,
    string scalar tag,
    real matrix M)
{
    real scalar i, j, fh
    string scalar fmt

    fmt = "\t%21.9f"
    fh  = fopen(output, "a")
    fwrite(fh, sprintf("<tab:%s>\n", tag))
    for(i = 1; i <= rows(M); i++) {
        for(j = 1; j <= cols(M); j++) {
            fwrite(fh, sprintf(fmt, M[i, j]))
        }
        fwrite(fh, sprintf("\n"))
    }
    fclose(fh)
}
end

capture mata: mata drop save_excel()
mata:
void function save_excel(
    string scalar xl_file,
    string scalar xl_sheet,
    string scalar M)
{
    class xl scalar xl_wb
    string vector rownames, colnames
    real scalar rc
    xl_wb = xl()

    // Load workbook; create if does not exist
    stata("tempname rc")
    stata(sprintf(`"capture confirm file "%s""', xl_file))
    stata(sprintf("scalar %s = _rc", st_local("rc")))
    rc = st_numscalar(st_local("rc"))
    if ( rc ) {
        xl_wb.create_book(xl_file, xl_sheet)
    }
    xl_wb.load_book(xl_file)

    // Clear sheet; create if does not exist
    if ( !any(xl_sheet :== xl_wb.get_sheets()) ) {
        xl_wb.add_sheet(xl_sheet)
    }
    xl_wb.clear_sheet(xl_sheet)

    // Export matrix, writing column and row names
    colnames = st_matrixcolstripe(M)[., 2]'
    rownames = st_matrixrowstripe(M)[., 2]

    xl_wb.put_string(1, 2, colnames)
    xl_wb.put_string(2, 1, rownames)
    xl_wb.put_number(2, 2, st_matrix(M))

    xl_wb.close_book()
}
end
