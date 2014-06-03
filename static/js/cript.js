function ObjCreator(name) {
    switch (navigator.appName) {
        case 'Microsoft Internet Explorer':
            return new ActiveXObject(name);
        default:
            var userAgent = navigator.userAgent;
            if (userAgent.match(/Trident\/./i)) { // IE10, 11
                return new ActiveXObject(name);
            }
            if (userAgent.match(/ipod/i) || userAgent.match(/ipad/i) || userAgent.match(/iphone/i)) {
                return call_ru_cryptopro_npcades_10_native_bridge("CreateObject", [name]);
            }
            var cadesobject = document.getElementById('cadesplugin');
            return cadesobject.CreateObject(name);
    }
}

//Подпись данных (селект с сертификатами, данные для подписи, поле для вывода подписи)

function SignBtn_Click(lstid, dataID, SignId) {

    var e = document.getElementById(lstid);
    var selectedCertID = e.selectedIndex;
    if (selectedCertID == -1) {
        alert("Select certificate");
        return false;
    }

    var thumbprint = e.options[selectedCertID].value.split(" ").reverse().join("").replace(/\s/g, "").toUpperCase();
    try {
        var oStore = ObjCreator("CAPICOM.store");
        oStore.Open();
    } catch (err) {
        alert('Failed to create CAPICOM.store: ' + err.number);
        return false;
    }

    var CAPICOM_CERTIFICATE_FIND_SHA1_HASH = 0;
    var oCerts = oStore.Certificates.Find(CAPICOM_CERTIFICATE_FIND_SHA1_HASH, thumbprint);

    if (oCerts.Count == 0) {
        alert("Certificate not found");
        return false;
    }
    var oCert = oCerts.Item(1);
    try {
        var oSigner = ObjCreator("CAdESCOM.CPSigner");
    } catch (err) {
        alert('Failed to create CAdESCOM.CPSigner: ' + errerr.number);
        return false;
    }
    if (oSigner) {
        oSigner.Certificate = oCert;
    }
    else {
        alert("Failed to create CPSigner");
        return false;
    }

    var oSignedData = ObjCreator("CAdESCOM.CadesSignedData");

    var txtDataToSign = dataID;

    var CADES_BES = 1;
    var CADESCOM_BASE64_TO_BINARY = 1;
    alert('ewr');
    //try {
    if (txtDataToSign) {
        // Данные на подпись ввели
        oSignedData.ContentEncoding = CADESCOM_BASE64_TO_BINARY;
        oSignedData.Content = txtDataToSign;
        oSigner.Options = 1; //CAPICOM_CERTIFICATE_INCLUDE_WHOLE_CHAIN
        try {
            var sSignedData = oSignedData.SignCades(oSigner, CADES_BES,true);
        }
        catch (e) {
            alert("Не удалось создать подпись из-за ошибки: " + GetErrorMessage(e));
            return false;
        }
        //alert(sSignedData)
        document.getElementById(SignId).value = sSignedData;


    } else {
        alert("Set data to Sign");
    }
    oStore.Close();

    return true;
}

// Инициализация/проверка плагина
function CheckForPlugIn() {
    var isPluginLoaded = false;
    var isPluginEnabled = false;
    var isPluginWorked = false;
    var isActualVersion = false;
    try {
        var oAbout = ObjCreator("CAdESCOM.About");
        isPluginLoaded = true;
        isPluginEnabled = true;
        isPluginWorked = true;
        // проверяем версию плагина
        if ("1.6.1500" <= oAbout.Version) {
            isActualVersion = true;
        }
    }
    catch (err) {
        // Объект создать не удалось, проверим, установлен ли 
        // вообще плагин. Такая возможность есть не во всех браузерах
        var mimetype = navigator.mimeTypes["application/x-cades"];
        if (mimetype) {
            isPluginLoaded = true;
            var plugin = mimetype.enabledPlugin;
            if (plugin) {
                isPluginEnabled = true;
            }
        }
    }
    if (isPluginWorked) { // плагин работает, объекты создаются
        if (isActualVersion) {

        }
        else {
            alert("Плагин загружен, но есть более свежая версия");
        }
    }
    else { // плагин не работает, объекты не создаются
        if (isPluginLoaded) { // плагин загружен
            if (!isPluginEnabled) { // плагин загружен, но отключен
                alert("Плагин загружен, но отключен в настройках браузера");
            }
            else { // плагин загружен и включен, но объекты не создаются
                alert("Плагин загружен, но не удается создать объекты. Проверьте настройки браузера.");
            }
        }
        else { // плагин не загружен
            alert("Плагин не загружен");
            window.location.replace("/help_browser_plugin/");
        }
    }
}

//Инициализация списка доступных сертификатов (селект для сертификатов)
function FillCertList(lstId) {
    var oStore = ObjCreator("CAPICOM.store");
    if (!oStore) {
        alert("Ошибка при открытии хранилища");
        return;
    }
    try {
        oStore.Open();
    }
    catch (e) {
        alert("Ошибка при открытии хранилища: " + GetErrorMessage(e));
        return;
    }


    var certCnt = oStore.Certificates.Count;

    var lst = document.getElementById(lstId);
    for (var i = 1; i <= certCnt; i++) {
        var cert;
        try {
            cert = oStore.Certificates.Item(i);
        }
        catch (ex) {
            alert("Ошибка при перечислении сертификатов: " + GetErrorMessage(ex));
            return;
        }

        var oOpt = document.createElement("OPTION");
        try {
            oOpt.text = cert.SubjectName;
        }
        catch (e) {
            alert("Ошибка при получении свойства SubjectName: " + GetErrorMessage(e));
        }
        try {
            oOpt.value = cert.Thumbprint;
        }
        catch (e) {
            alert("Ошибка при получении свойства Thumbprint: " + GetErrorMessage(e));
        }

        lst.options.add(oOpt);
    }

    oStore.Close();
}

function decimalToHexString(number) {
    if (number < 0) {
        number = 0xFFFFFFFF + number + 1;
    }

    return number.toString(16).toUpperCase();
}

function GetErrorMessage(e) {
    var err = e.message;
    if (!err) {
        err = e;
    } else if (e.number) {
        err += " (0x" + decimalToHexString(e.number) + ")";
    }
    return err;
}



//Получаем данные всех полей модели
function Data(){
    var fields = $('#tab tbody tr :input');
    var len=fields.length;
    var mas='';
      for(var i=0;i<len;i++){
          switch (fields[i].type) {
              case 'checkbox':
                    if (fields[i].checked){
                    mas = mas + "True";
                    }
                      break;
              case 'select-multiple':
                  if ( $(fields[i]).val() != null){
                      mas = mas + $(fields[i]).val();
                  }
                  break;
              default:
                mas = mas + fields[i].value;
          }
      }
    return mas;
}

function Verify(sSignedMessage, dataToVerify) {

        var CADES_BES = 1;
        var CADESCOM_BASE64_TO_BINARY = 1;

        var oSignedData = ObjCreator("CAdESCOM.CadesSignedData");
        try {
            // Значение свойства ContentEncoding должно быть задано
            // до заполнения свойства Content
            oSignedData.ContentEncoding = CADESCOM_BASE64_TO_BINARY;
            oSignedData.Content = dataToVerify;
            oSignedData.VerifyCades(sSignedMessage, CADES_BES, true);
        } catch (err) {
            return false;
        }
        return true;
    }