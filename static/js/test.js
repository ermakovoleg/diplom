var CADESCOM_CADES_X_LONG_TYPE_1 = 0x5d;
        var CADESCOM_BASE64_TO_BINARY = 1;


        function SignCreate(certSubjectName, dataToSign) {
            var oStore = CreateObject("CAPICOM.Store");
            oStore.Open(CAPICOM_CURRENT_USER_STORE, CAPICOM_MY_STORE,
            CAPICOM_STORE_OPEN_MAXIMUM_ALLOWED);

            var oCertificates = oStore.Certificates.Find(
            CAPICOM_CERTIFICATE_FIND_SUBJECT_NAME, certSubjectName);
            if (oCertificates.Count == 0) {
                alert("Certificate not found: " + certSubjectName);
                return;
            }
            var oCertificate = oCertificates.Item(1);
            var oSigner = CreateObject("CAdESCOM.CPSigner");
            oSigner.Certificate = oCertificate;
            oSigner.TSAAddress = "http://cryptopro.ru/tsp/";

            var oSignedData = CreateObject("CAdESCOM.CadesSignedData");
            oSignedData.Content = dataToSign;

            try {
                var sSignedMessage = oSignedData.SignCades(oSigner, CADESCOM_CADES_X_LONG_TYPE_1);
            } catch (err) {
                alert("Failed to create signature. Error: " + GetErrorMessage(err));
                return;
            }

            oStore.Close();

            return sSignedMessage;
        }

        function Verify(sSignedMessage) {
            var oSignedData = CreateObject("CAdESCOM.CadesSignedData");
            try {
                oSignedData.VerifyCades(sSignedMessage, CADESCOM_CADES_X_LONG_TYPE_1);
            } catch (err) {
                alert("Failed to verify signature. Error: " + GetErrorMessage(err));
                return false;
            }

            return true;
        }

        function run() {

                    // Предварительно закодированные в BASE64 бинарные данные
                    // В данном случае закодирована строка "Some Data."
                    var dataInBase64 = "U29tZSBEYXRhLg==";

            var signedMessage = SignCreate(sCertName, "Message");

                    var signedMessage = SignCreate(sCertName, dataInBase64);

            document.getElementById("signature").innerHTML = signedMessage;

            var verifyResult = Verify(signedMessage);

                    var verifyResult = Verify(signedMessage, dataInBase64);

            if (verifyResult) {
                alert("Signature verified");
            }
        }




    function SignCreate(certSubjectName, dataToSign) {



                    // Значение свойства ContentEncoding должно быть задано
                    // до заполнения свойства Content
                    oSignedData.ContentEncoding = CADESCOM_BASE64_TO_BINARY;
                    oSignedData.Content = dataToSign;


                    sSignedMessage = oSignedData.SignCades(oSigner, CADESCOM_CADES_BES, true);




        return sSignedMessage;
    }

    function Verify(sSignedMessage, dataToVerify) {
        var oSignedData = CreateObject("CAdESCOM.CadesSignedData");
        try {
            // Значение свойства ContentEncoding должно быть задано
            // до заполнения свойства Content
            oSignedData.ContentEncoding = CADESCOM_BASE64_TO_BINARY;
            oSignedData.Content = dataToVerify;
            oSignedData.VerifyCades(sSignedMessage, CADESCOM_CADES_BES, true);
        } catch (err) {
            alert("Failed to verify signature. Error: " + GetErrorMessage(err));
            return false;
        }

        return true;
    }

