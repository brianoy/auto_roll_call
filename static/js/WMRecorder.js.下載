//----------------------------------------------------------------------
/*
 class WMRecorder
 {
 public:
  obj stobj
  obj psobj
  obj spobj

  void AttachButton(startbutton, pausebutton, stopbutton);
  void AttachComponent(recorder);
 }
*/

//----------------------------------------------------------------------
function _SetState(StateCode)
{
	switch (StateCode)
	{
	case 0:
		this.stobj.disabled = false;
		this.psobj.disabled = true;
		this.spobj.disabled = true;
		break;

	case 2:
		this.stobj.disabled = false;
		this.psobj.disabled = true;
		this.spobj.disabled = false;
		break;

	case 1:
		this.stobj.disabled = true;
		this.psobj.disabled = false;
		this.spobj.disabled = false;
		break;

	}
}
//----------------------------------------------------------------------
function StartClick()
{
	eval(this.recobj+".recorder.StartRec()");	
	eval(this.recobj+".SetState(1)");
	eval(this.recobj+".IsRec = true");
	//eval("alert("+this.recobj+".recorder.RecFilename);")
	//alert(this.recobj);
	//this.recorder.StartRec();
	//this.SetState(1);
}
//----------------------------------------------------------------------
function PauseClick()
{
	eval(this.recobj+".recorder.PauseRec()");
	eval(this.recobj+".SetState(2)");

	//this.recorder.PauseRec();
	//this.SetState(2);
}
//----------------------------------------------------------------------
function StopClick()
{
	eval(this.recobj+".recorder.StopRec()");
	eval(this.recobj+".SetState(0)");

	//this.recorder.StopRec();
	//this.SetState(0);
}
//----------------------------------------------------------------------
/*
function _FormSubmit()
{
	var aa, bb, upr;
	//if ( !(g_WMRecorder.Send()) ) return false;
	alert(this.recobj);
	
	eval("bb = "+this.recobj+".IsRec;");
	
	//eval("if ( !("+this.recobj+".Send()) ) return false;");
	eval("aa = "+this.recobj+".Send();");
	
	//eval("if ( !("+this.recobj+".IsRec) ) return false;");	
	
	
	//g_WMRecorder.Send();

	alert(bb);
	if ( aa && bb )
	{
		eval("upr ="+this.recobj+".UploadResult");
		if ( upr != "" )
		{
				eval(this.recobj+".HTMLForm.mp3path.value=upr");
		}
	}
	
	eval(this.recobj+".DefaultFormSumit()");
	
	//g_WMRecorder.HTMLForm.mp3path.value = g_WMRecorder.UploadResult;	
	//g_WMRecorder.DefaultFormSumit();
}
*/
//----------------------------------------------------------------------
/*
function _AttachForm(HTMLForm)
{
	if ( HTMLForm == null ) return;

	objnameitem = document.createAttribute("recobj")
	objnameitem.value = this.objname;

	this.DefaultFormSumit = HTMLForm.onsubmit;
	HTMLForm.onsubmit = _FormSubmit;
	this.HTMLForm = HTMLForm;
	this.HTMLForm.attributes.setNamedItem(objnameitem);
}
*/
//----------------------------------------------------------------------
function _AttachButton(startbutton, pausebutton, stopbutton)
{
	if (( startbutton == null ) || ( pausebutton == null ) || ( stopbutton == null )) return;

	objnameitem = document.createAttribute("recobj")
	objnameitem.value = this.objname;
	
	this.stobj = startbutton;
	this.stobj.onclick = StartClick;
	this.stobj.attributes.setNamedItem(objnameitem);

	objnameitem = document.createAttribute("recobj")
	objnameitem.value = this.objname;

	this.psobj = pausebutton;
	this.psobj.onclick = PauseClick;
	this.psobj.attributes.setNamedItem(objnameitem);

	objnameitem = document.createAttribute("recobj")
	objnameitem.value = this.objname;

	this.spobj = stopbutton;
	this.spobj.onclick = StopClick;
	this.spobj.attributes.setNamedItem(objnameitem);
}
//----------------------------------------------------------------------
function _AttachComponent(recorder)
{
	if ( recorder == null ) return;
	this.recorder = recorder;

	this.recorder.RecFile = this.RecFile;
	this.recorder.TimeLimit = this.TimeLimit;
	this.SetState(0);
}
//----------------------------------------------------------------------
function _SetPostURI(PostURI)
{
	if ( PostURI == "" ) return;
	this.PostURI = PostURI;
}
//----------------------------------------------------------------------
function _SetPostData(Cookie, BID, CID)
{
	if ( (Cookie == "") || (BID == "")) return;
	this.Cookie = Cookie;
	this.BID = BID;
	this.CID = CID;
}
//----------------------------------------------------------------------
function _Send()
{
	var rtval = false;
	if ( this.recorder )
	{
		//if ( this.StateCode != 0 ) StopClick();
		if (!this.IsRec) return rtval;
		
		this.recorder.PostURI = this.PostURI;
		this.recorder.WM_BoardID = this.BID;
		this.recorder.WM_CourseID = this.CID;	
		this.recorder.WM_Cookie = this.Cookie;
		
		try
		{
			this.recorder.UploadFile();
			this.UploadResult = this.recorder.UploadResult;
			if ( this.UploadResult == "" ) throw "Upload Failed.";
			return true;
		}
		catch (e)
		{
			alert(1);
			alert("Anicam Sound Recorder Error: " + e.description);
		}

	}
	else
	{
		alert("Anicam Sound Recorder Error: No Recorder");
	}
	return rtval;
}
//----------------------------------------------------------------------
function _SetRecFile(FileName)
{
	if ( FileName == "" ) return;
	this.RecFile = FileName;
}
//----------------------------------------------------------------------
function _SetTimeLimit(TimeLimit)
{
	this.TimeLimit = TimeLimit;
}
//----------------------------------------------------------------------
function WMRecorder()
{
	this.stobj = null;
	this.psobj = null;
	this.spobj = null;
	this.recorder = null;
	this.HTMLForm = null;
	//this.DefaultFormSubmit = null;
	this.PostURI = "";
	this.Cookie = "";
	this.BID = "";
	this.CID = "";
	this.RecFile = "c:\\temp.mp3";
	this.TimeLimit = 1;
	this.UploadResult = "";
	this.StateCode = 0;
	this.objname = "";
	this.IsRec = false;

	this.AttachButton = _AttachButton;
	this.AttachComponent = _AttachComponent;
	//this.AttachForm = _AttachForm;
	this.SetPostURI = _SetPostURI;
	this.SetPostData = _SetPostData;
	this.Send = _Send;
	this.SetRecFile = _SetRecFile;
	this.SetTimeLimit = _SetTimeLimit;
	this.SetState = _SetState;
}
//----------------------------------------------------------------------
//   class RecorderList
//
//
//
//
//
//----------------------------------------------------------------------
function _AddRecorder(recobjval)
{
	this.objcollect[this.count] = recobjval;
	this.count++;
}
//----------------------------------------------------------------------
function _OutputTo(objval)
{
	try
	{
		if ( objval == null ) throw "form error";

		//this.DefaultFormSumit = formval.onsubmit;
		//formval.onsubmit = _FormSubmit;
		this.HTMLFormVal = objval;
	}
	catch (err)
	{
		alert(2);
		alert("Anicam Sound Recorder Error: " + err.description);
	}
}
//----------------------------------------------------------------------
function _SendData()
{
	var objval;
	var result = "";
	var cnt = 0;
	
	for (i = 0; i < this.objcollect.length; ++i)
	{
		objval = this.objcollect[i];
		try
		{
			if ( objval.Send() )
			{
				if (cnt > 0)
				{
					result += ";" + result;
				}
				else
				{
					result = objval.UploadResult;
				}
				cnt++
			}
		}
		catch(err)
		{
			alert(3);
			alert("Anicam Sound Recorder Error: " + err.description);
			return false;
		}
	}
	if ( result != "" )
	{
		this.HTMLFormVal.value = result;
	}
	return true;
}
//----------------------------------------------------------------------
function RecorderList()
{
	// property
	this.count = 0;
	//this.DefaultFormSubmit = null;
	this.HTMLFormVal = null;
	this.objcollect = new Array();
	
	// method
	this.AddRecorder = _AddRecorder;
	this.OutputTo = _OutputTo;
	this.SendData = _SendData;
}
//----------------------------------------------------------------------
