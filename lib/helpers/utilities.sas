%macro sendMail(stime, prog);
    %if &syserr. ne 0 %then %do;
        %let paux = ran with errors [Automated Message];
        %let err  = ERROR: %bquote(&SYSERRORTEXT);
        %let warn = WARNING: %bquote(&SYSWARNINGTEXT);
    %end;
    %else %do;
        %let paux = ran [Automated Message];
        %let err  = ;
        %let warn = ;
    %end;
    %let etime = %sysfunc(putn(%sysfunc(datetime()), datetime.));
    %let msg   = &prog. finished running\n&err.\n&warn.\nStart: &stime.\nEnd: &etime.;
    %sysexec echo -e "&msg." | mail -s "&prog. &paux." &sysuserid.@nber.org;
%exit: %mend sendMail;


%macro assert(condition, handle = 1) / mindelimiter = '|';
    %if %eval(&condition.) ne 1 %then %do;
        %put ERROR: Assertion error;
        %put ERROR- &condition.;
        %goto errorHandle&handle.;
    %end;
    %else %goto exit;

    %errorHandle1:
        /*Statements if there are errors and execution will halt*/
        %abort cancel; %goto exit;

    %errorHandle2:
        /*Statements if there are errors SAS will exit (e.g. e-mail analyst, etc.)*/
        %abort abend; %goto exit;
%exit: %mend assert;


%macro genYM(prefix, dstart, dend, by);
    %let s = %sysfunc(intnx(&by, %sysfunc(inputn(01JAN&dstart, date9.)), 0, e));
    %let e = %sysfunc(intnx(&by, %sysfunc(inputn(31DEC&dend,   date9.)), 0, e));
    %do %while (%sysfunc(intck(&by, &s, &e)) gt -1);
        &prefix.%sysfunc(year(&s))m%sysfunc(month(&s))
        %let s = %sysfunc(intnx(&by, &s, 1, e));
    %end;
%exit: %mend genYM;


%macro macarray(varname, values, sep=%str( ));
    %global n&varname;
	%let n&varname = %sysfunc(countw(&values));
	%do i = 1 %to &&n&varname;
		%global &varname&i;
		%let &varname&i = %unquote(%qscan(&values, &i, &sep));
		%let &varname&i = %sysfunc(compress(%superq(&varname&i)));
	%end;
%mend macarray;
