var _formula = function (){
    var self= this;
    var debug = false;
    
    self.s010 = function() {
        var i;
        if (isAfrican() && isFemale()) i = 0.95334;
        if (!isAfrican() && isFemale()) i = 0.96652;
        if (isAfrican() && isMale()) i = 0.89536;
        if (!isAfrican() && isMale()) i = 0.91436;
        return i;
    };
    
    self.mnxb = function() {
        var i;
        if (isAfrican() && isFemale()) i = 86.61;
        if (!isAfrican() && isFemale()) i = -29.18;
        if (isAfrican() && isMale()) i = 19.54;
        if (!isAfrican() && isMale()) i = 61.18;
        return i;
    };

    //Optimal Values using baseline
    self.lnage = function() {
        if(isFollowUp())
            return Math.log(BaselineAge());
        else
            return Math.log(Age());
    };
    self.lnBaseLineUpage = function() {
        return Math.log(BaselineAge());
    };

    self.lnFollowUpage = function() {
        return Math.log(Age());
    };
    self.opt_lnhdl = function() {
        return Math.log(60);
    };
    self.opt_lntot = function() {
        return Math.log(170);
    };
    self.opt_trlnsbp = function() {
        return Math.log(110) * Number(false)
    };
    self.opt_ntlnsbp = function() {
        return Math.log(110) * Number(!false)
    };
    self.opt_age2 = function(isFollowUp) {
        if(isFollowUp)
            return self.lnFollowUpage() * self.lnFollowUpage();
        else
            return self.lnage() * self.lnage();
    };
    self.opt_agetc = function(isFollowUp) {
        if(isFollowUp)
            return self.opt_lntot() * self.lnFollowUpage();
        else
            return self.opt_lntot() * self.lnage();
    };
    self.opt_agehdl = function(isFollowUp) {
        if(isFollowUp)
            return self.opt_lnhdl() * self.lnFollowUpage();
        else
            return self.opt_lnhdl() * self.lnage();
    };
    self.opt_agetsbp = function(isFollowUp) {
        if(isFollowUp)
            return self.lnFollowUpage() * self.opt_trlnsbp();
        else
            return self.lnage() * self.opt_trlnsbp();
    };
    self.opt_agentsbp = function(isFollowUp) {
        if(isFollowUp)
            return self.lnFollowUpage() * self.opt_ntlnsbp();
        else
            return self.lnage() * self.opt_ntlnsbp();
    };
    self.otp_agesmoke = function() {
        return self.lnage() * Number(false);
    };
    self.opt_agedm = function() {
        return self.lnage() * Number(false);
    };

    self.optimalPredictCalculate = function(isFollowUp) {
        var i;
        if (isAfrican() && isFemale() )
            i = 17.1141 * (isFollowUp
                ? self.lnFollowUpage()
                : self.lnage())
                + 0.9396 * self.opt_lntot()
                + (-18.9196 * self.opt_lnhdl())
                + 4.4748 * self.opt_agehdl(isFollowUp)
                + 29.2907 * self.opt_trlnsbp()
                + (-6.4321 * self.opt_agetsbp(isFollowUp))
                + 27.8197 * self.opt_ntlnsbp()
                + (-6.0873 * self.opt_agentsbp(isFollowUp))
                + 0.6908 * Number(false)
                + 0.8738 * Number(false);

        if (!isAfrican() && isFemale() )
            i = (-29.799 * (isFollowUp ? self.lnFollowUpage()
                : self.lnage()))
                + 4.884 * self.opt_age2()
                + 13.54 * self.opt_lntot()
                + (-3.114 * self.opt_agetc(isFollowUp))
                + (-13.578 * self.opt_lnhdl())
                + 3.149 * self.opt_agehdl(isFollowUp)
                + 2.019 * self.opt_trlnsbp()
                + 1.957 * self.opt_ntlnsbp()
                + 7.574 * Number(false)
                + (-1.665 * self.otp_agesmoke(isFollowUp))
                + 0.661 * Number(false);

        if (isAfrican() && isMale())
            i = 2.469 * (isFollowUp ? self.lnFollowUpage()
                : self.lnage())
                + 0.302 * self.opt_lntot()
                + (-0.307 * self.opt_lnhdl())
                + 1.916 * self.opt_trlnsbp()
                + 1.809 * self.opt_ntlnsbp()
                + 0.549 * Number(false)
                + 0.645 * Number(false);

        if (!isAfrican() && isMale())
            i = 12.344 * (isFollowUp ? self.lnFollowUpage()
                : self.lnage())
                + 11.853 * self.opt_lntot()
                + (-2.664 * self.opt_agetc(isFollowUp))
                + (-7.99 * self.opt_lnhdl())
                + 1.769 * self.opt_agehdl(isFollowUp)
                + 1.797 * self.opt_trlnsbp()
                + 1.764 * self.opt_ntlnsbp()
                + 7.837 * Number(false)
                + (-1.795 * self.otp_agesmoke(isFollowUp))
                + 0.658 * Number(false);

        if(debug)
            console.log(i);

        return i;
    };

    self.optimalCvdPredict = function(isFollowUp) {
        var i;
        i= (1 - Math.pow(self.s010(), Math.exp( self.optimalPredictCalculate(isFollowUp) - self.mnxb())));
        if (debug)
            console.log(i);

        return i;
    };
    //Sheet(10-Year ASCVD Follow up) OPTIMAL Floor Value derived using the OPTIMAL level - G28
    self.optimalBaselineRisk = function(){
        var i = '~%';
        var predValue = self.optimalCvdPredict(false);
        if (predValue != 1 && !isNaN(predValue)) {
            var number = predValue * 100
            if (debug)
                console.log(number);

            i = number.toFixed(1) + '%';
        }
        return i;
    };
    //Sheet(10-Year ASCVD Follow up) OPTIMAL Floor Value derived UPDATED AGE - G59
    self.optimalFollowUpRisk = function(){
        var i = '~%';
        var predValue = self.optimalCvdPredict(true);
        if (predValue != 1 && !isNaN(predValue)) {
            var number = predValue * 100
            i = number.toFixed(1) + '%';
        }
        return i;
    };

    //ASCVD Risk calculation factors
    self.lnhdl = function(isCurrent) {
        if(isCurrent)
            return Math.log(HDLCholesterol());
        else
            return Math.log(BaselineHDLCholesterol());
    };
    self.lntot = function(isCurrent) {
        if(isCurrent)
            return Math.log(TotalCholesterol());
        else
            return Math.log(BaselineTotalCholesterol());
    };
    self.trlnsbp = function(isCurrent) {
        if(isCurrent)
            return Math.log(BloodPressure()) * Number(isHypertension());
        else
            return Math.log(BaselineBloodPressure()) * Number(isBaseLineHypertension());
    };
    self.ntlnsbp = function(isCurrent) {
        if(isCurrent)
            return Math.log(BloodPressure()) * Number(!isHypertension());
        else
            return Math.log(BaselineBloodPressure()) * Number(!isBaseLineHypertension());
    };
    self.age2 = function(isCurrent) {
        if(isCurrent)
            return self.lnFollowUpage() * self.lnFollowUpage();
        else
            return self.lnage() * self.lnage();
    };
    self.agetc = function(isCurrent) {
        if(isCurrent)
            return self.lntot(isCurrent) * self.lnFollowUpage();
        else
            return self.lntot() * self.lnage();
    };
    self.agehdl = function(isCurrent) {
        if(isCurrent)
            return self.lnhdl(isCurrent) * self.lnFollowUpage();
        else
            return self.lnhdl() * self.lnage();
    };
    self.agetsbp = function(isCurrent) {
        if(isCurrent)
            return self.lnFollowUpage() * self.trlnsbp(isCurrent);
        else
            return self.lnage() * self.trlnsbp();
    };
    self.agentsbp = function(isCurrent) {
        if(isCurrent)
            return self.lnFollowUpage() * self.ntlnsbp(isCurrent);
        else
            return self.lnage() * self.ntlnsbp();
    };
    //Need to check smoker case in case of baseline
    self.agesmoke = function(isCurrent) {
        if(isCurrent)
            return self.lnFollowUpage() * Number(isSmoker());
        else
            return self.lnage() * Number(isBaseLineSmoker());
    };
    self.agedm = function(isCurrent) {
        if(isCurrent)
            return self.lnFollowUpage() * Number(isDiabetic());
        else
            return self.lnage() * Number(isBaseLineDiabetic());
    };

    //Need to check baseline diabetic and smoker values
    self.predictCalculate = function(isCurrent) {
        var i;
        if (isAfrican() && isFemale() )
            i = 17.1141 * (isCurrent ? self.lnFollowUpage(): self.lnage())
                + 0.9396 * self.lntot(isCurrent)
                + (-18.9196 * self.lnhdl(isCurrent))
                + 4.4748 * self.agehdl(isCurrent)
                + 29.2907 * self.trlnsbp(isCurrent)
                + (-6.4321 * self.agetsbp(isCurrent))
                + 27.8197 * self.ntlnsbp(isCurrent)
                + (-6.0873 * self.agentsbp(isCurrent))
                + 0.6908 * (isCurrent ? Number(isSmoker()):Number(isBaseLineSmoker()))
                + 0.8738 * (isCurrent ? Number(isDiabetic()):Number(isBaseLineDiabetic()))

        if (!isAfrican() && isFemale() )
            i = (-29.799 * (isCurrent ? self.lnFollowUpage(): self.lnage()))
                + 4.884 * self.age2(isCurrent) + 13.54 * self.lntot(isCurrent)
                + (-3.114 * self.agetc(isCurrent))
                + (-13.578 * self.lnhdl(isCurrent))
                + 3.149 * self.agehdl(isCurrent)
                + 2.019 * self.trlnsbp(isCurrent)
                + 1.957 * self.ntlnsbp(isCurrent)
                + 7.574 * (isCurrent ? Number(isSmoker()):Number(isBaseLineSmoker()))
                + (-1.665 * self.agesmoke(isCurrent))
                + 0.661 * (isCurrent ? Number(isDiabetic()):Number(isBaseLineDiabetic()));

        if (isAfrican() && isMale())
            i = 2.469 * (isCurrent ? self.lnFollowUpage(): self.lnage())
                + 0.302 * self.lntot(isCurrent)
                + (-0.307 * self.lnhdl(isCurrent))
                + 1.916 * self.trlnsbp(isCurrent)
                + 1.809 * self.ntlnsbp(isCurrent)
                + 0.549 * (isCurrent ? Number(isSmoker()):Number(isBaseLineSmoker()))
                + 0.645 * (isCurrent ? Number(isDiabetic()):Number(isBaseLineDiabetic()));

        if (!isAfrican() && isMale())
            i = 12.344 * (isCurrent ? self.lnFollowUpage(): self.lnage())
                + 11.853 * self.lntot(isCurrent)
                + (-2.664 * self.agetc(isCurrent))
                + (-7.99 * self.lnhdl(isCurrent))
                + 1.769 * self.agehdl(isCurrent)
                + 1.797 * self.trlnsbp(isCurrent)
                + 1.764 * self.ntlnsbp(isCurrent)
                + 7.837 * (isCurrent ? Number(isSmoker()):Number(isBaseLineSmoker()))
                + (-1.795 * self.agesmoke(isCurrent))
                + 0.658 * (isCurrent ? Number(isDiabetic()):Number(isBaseLineDiabetic()));

        if(debug)
            console.log(i);

        return i;
    };

    //updated estimates trlnsbp and ntlnsbp
    self.up_trlnsbp = function() {
        return Math.log(BaselineBloodPressure()) * Number(isHypertension());
    };
    self.up_ntlnsbp = function() {
        return Math.log(BaselineBloodPressure()) * Number(!isHypertension());
    };
    self.up_agetsbp = function() {
        return self.lnFollowUpage() * self.up_trlnsbp();
    };
    //This takes only updated age and use baseline values and Need to check isDiabetic
    self.updatedPredictCalculate = function() {
        var i;
        if (isAfrican() && isFemale() ) {
            i = 17.1141 * self.lnFollowUpage() + 0.9396 * self.lntot(false) + (-18.9196 * self.lnhdl(false)) + 4.4748 * (Math.log(BaselineHDLCholesterol()) * self.lnFollowUpage()) + 29.2907 * self.up_trlnsbp() + (-6.4321 * self.up_agetsbp()) + 27.8197 * self.up_ntlnsbp() + (-6.0873 * (self.up_ntlnsbp() * self.lnFollowUpage())) + 0.6908 * Number(isSmoker()) + 0.8738 * Number(isDiabetic());
        }
        if (!isAfrican() && isFemale() )
            i = (-29.799 * self.lnFollowUpage()) + 4.884 * self.age2(true) + 13.54 * self.lntot(false) + (-3.114 * (self.lntot(false) * self.lnFollowUpage())) + (-13.578 * self.lnhdl(false)) + 3.149 * (self.lnhdl(false) * self.lnFollowUpage()) + 2.019 * self.up_trlnsbp() + 1.957 * self.up_ntlnsbp() + 7.574 * Number(isSmoker()) + (-1.665 * (self.lnFollowUpage() * Number(isSmoker()))) + 0.661 * Number(isDiabetic());
        if (isAfrican() && isMale())
            i = 2.469 * self.lnFollowUpage() + 0.302 * self.lntot(false) + (-0.307 * self.lnhdl(false)) + 1.916 * self.up_trlnsbp() + 1.809 * self.up_ntlnsbp() + 0.549 * Number(isSmoker()) + 0.645 * Number(isDiabetic());
        if (!isAfrican() && isMale())
            i = 12.344 * self.lnFollowUpage() + 11.853 * self.lntot(false) + (-2.664 * (self.lntot(false) * self.lnFollowUpage())) + (-7.99 * self.lnhdl(false)) + 1.769 * (self.lnhdl(false) * self.lnFollowUpage()) + 1.797 * self.up_trlnsbp() + 1.764 * self.up_ntlnsbp() + 7.837 * Number(isSmoker()) + (-1.795 * (self.lnFollowUpage() * Number(isSmoker()))) + 0.658 * Number(isDiabetic());
        if(debug)
            console.log(i);

        return i;
    };

    //Calculates CVD predict for baseline and current values
    self.cvdPredict = function(isCurrent) {
        var i;
        i= (1 - Math.pow(self.s010(), Math.exp( self.predictCalculate(isCurrent) - self.mnxb())));
        if(debug)
            console.log(i);

        return i;
    };
    //Sheet(10-Year Expected ASCVD) 10-Year ASCVD Risk at Baseline - G29
    self.TenYearBaselineRisk = function(){
        var i = '~%';
        var predValue = self.cvdPredict(false);
        if (predValue != 1 && !isNaN(predValue)) {
            var number = predValue * 100
            if(debug)
                console.log(number);

            i = number.toFixed(1) + '%';
        }
        return i;
    };
    //Sheet(10-Year ASCVD Follow up) 10-Year ASCVD floor for follow up - G92
    self.TenYearRiskUsingFollowUpValue = function(){
        var i = '~%';
        var predValue = self.cvdPredict(true);
        if (predValue != 1 && !isNaN(predValue)) {
            var number = predValue * 100
            i = number.toFixed(1) + '%';
        }
        return i;
    };

    self.updatedCvdPredict = function() {
        var i;
        i= (1 - Math.pow(self.s010(), Math.exp( self.updatedPredictCalculate() - self.mnxb())));
        if(debug)
            console.log("e125 => ",i, " s010 => ",self.s010(), " mnxb => ",self.mnxb(), " d125 => ", self.updatedPredictCalculate());

        return i;
    };
    //Sheet(10-Year ASCVD Follow up) Updated Estimates - G125
    self.TenYearRiskUsingUpdatedEstimates = function(){
        var i = '~%';
        var predValue = self.updatedCvdPredict();
        if (predValue != 1 && !isNaN(predValue)) {
            var number = predValue * 100
            i = number.toFixed(1) + '%';
        }
        return i;
    };

    // Relative Risk calculations
    self.relativeRiskStatin = 0.75;
    self.relativeRiskBP = Math.exp((Math.log(0.84) + Math.log(0.64))/2);
    self.relativeRiskStopSmoking=0.73;
    self.relativeRiskAspirin = 0.90;
    self.relativeRiskAspirinStatin = (self.relativeRiskStatin * self.relativeRiskAspirin);
    self.relativeRiskAspirinBP = (self.relativeRiskBP * self.relativeRiskAspirin);
    self.relativeRiskStatinBP = (self.relativeRiskStatin * self.relativeRiskBP);
    self.relativeRiskStatinStopSmoking = (self.relativeRiskStatin * self.relativeRiskStopSmoking);
    self.relativeRiskAspirinStopSmoking = (self.relativeRiskAspirin * self.relativeRiskStopSmoking);
    self.relativeRiskBPStopSmoking = (Math.exp((Math.log(0.84) + Math.log(0.64))/2) * 0.73);
    self.relativeRiskStatinAspirinBP = (self.relativeRiskStatin * self.relativeRiskBP * self.relativeRiskAspirin);
    self.relativeRiskAspirinBPStopSmoking = (self.relativeRiskBP * self.relativeRiskStopSmoking * self.relativeRiskAspirin);
    self.relativeRiskStatinBPStopSmoking = (self.relativeRiskBP * self.relativeRiskStopSmoking * self.relativeRiskStatin);
    self.relativeRiskAspirinStatinStopSmoking = (self.relativeRiskAspirin * self.relativeRiskStopSmoking * self.relativeRiskStatin);
    self.relativeRiskAll4 = (self.relativeRiskStatin * self.relativeRiskAspirin * self.relativeRiskStopSmoking * self.relativeRiskBP);
    self.relativeRiskFollowupBP = Math.exp((Math.log(0.79) + Math.log(0.54))/2).toFixed(2);

    //Delta Calculations
    self.statinDelta = function(){
        if(LDLCholesterol()){
            return	Math.pow(self.relativeRiskStatin,((BaselineLDLCholesterol() - LDLCholesterol())/38.7));
        }
    };
    self.bloodPresureDelta = function(){
        if(BloodPressure()){
            return	Math.pow( Math.exp((Math.log(0.79) + Math.log(0.54))/2),((BaselineBloodPressure() - BloodPressure())/10));
        }
    };

    self.smokerDelta = function(){
        if(!isBaseLineSmoker() || !QuiteSmokingMonths()){
            return 1;
        }else if(QuiteSmokingMonths()){
            return QuiteSmokingMonths().value;
        }
        else {
            return 1;
        }
    };
    self.aspirinDelta = function(){
        if(OnAspirin() == 'Yes'){
            return 0.9;
        }else{
            return 1;
        }
    };
    //Sheet(10-Year ASCVD Follow up) all therapy delta - G119
    self.summationDelta = function(){
        return self.statinDelta() * self.bloodPresureDelta() * self.smokerDelta() * self.aspirinDelta();
    };
    //Sheet(10-Year ASCVD Follow up) 10-Year ASCVD with delta and updated estimates - H125
    self.TenYearRiskWithUpdatedEstimatesDelta = function(){
        var g125 = self.updatedCvdPredict();
        var g119 = self.summationDelta();
        if(debug)
            console.log("g125 => ", g125," g119 => ",g119);

        return g125 * g119;
        //return self.updatedCvdPredict() * self.summationDelta();
    };
    //Sheet(Updated RR) 10-Year ASCVD follow up - C19
    self.TenYearFollowUpRisk = function(){
        var h125 = self.TenYearRiskWithUpdatedEstimatesDelta();
        var g59 = self.optimalCvdPredict(true);
        var g92 = self.cvdPredict(true);
        var number =  Math.min(Math.max(h125,g59), g92) * 100;
        return number.toFixed(1) + '%';
    };
    //start: Forecasted Risk at Initial Visit(Expected RR sheet)
    self.ForecastRiskStatin = function(){
        var baselineRisk = isFollowUp() ? self.cvdPredict(false) :self.cvdPredict(true);
        var optimalBaseline = self.optimalCvdPredict(false);
        if(baselineRisk < 0.05){
            return 'NA';
        }else{
            return Math.max(baselineRisk * self.relativeRiskStatin, optimalBaseline);
        }
    };
    self.ForecastRiskBP = function(){
        var baselineRisk = isFollowUp() ? self.cvdPredict(false) :self.cvdPredict(true);
        var optimalBaseline = self.optimalCvdPredict(false);
        var bp = isFollowUp() ? BaselineBloodPressure() : BloodPressure();
        var diabetic = isFollowUp() ? BaselineDiabetic() : Diabetic();
        if(bp < 120 || (diabetic == 'Yes' && bp < 130)){
            return 'NA';
        }else{
            return Math.max(baselineRisk * self.relativeRiskBP, optimalBaseline);
        }
    };
    self.ForecastRiskSmoking = function(){
        var baselineRisk = isFollowUp() ? self.cvdPredict(false) : self.cvdPredict(true);
        var optimalBaseline = self.optimalCvdPredict(false);
        var smoke = isFollowUp() ? BaselineSmoker() : Smoker();

        if(smoke == 'No' || smoke == 'Never'){
            return 'NA';
        }else{
            return Math.max(baselineRisk * self.relativeRiskStopSmoking, optimalBaseline);
        }
    };
    self.ForecastRiskAspirin = function(){
        var baselineRisk = isFollowUp() ? self.cvdPredict(false) : self.cvdPredict(true);
        var optimalBaseline = self.optimalCvdPredict(false);
        if(baselineRisk < 0.1){
            return 'NA';
        }else{
            return Math.max(baselineRisk * self.relativeRiskAspirin, optimalBaseline);
        }
    };
    self.ForecastRiskAspirinStatin = function(){
        var baselineRisk = isFollowUp() ? self.cvdPredict(false) : self.cvdPredict(true);
        var optimalBaseline = self.optimalCvdPredict(false);
        if(baselineRisk < 0.1){
            return 'NA';
        }else{
            return Math.max(baselineRisk * self.relativeRiskAspirinStatin, optimalBaseline);
        }
    };
    self.ForecastRiskAspirinBP = function(){
        var baselineRisk = isFollowUp() ? self.cvdPredict(false) : self.cvdPredict(true);
        var optimalBaseline = self.optimalCvdPredict(false);
        var bp = isFollowUp() ? BaselineBloodPressure() : BloodPressure();
        var diabetic = isFollowUp() ? BaselineDiabetic() : Diabetic();
        if(baselineRisk < 0.1 || (bp < 120 || (diabetic == 'Yes' && bp < 130))){
            return 'NA';
        }else{
            return Math.max(baselineRisk * self.relativeRiskAspirinBP, optimalBaseline);
        }
    };
    self.ForecastRiskStatinBP = function(){
        var baselineRisk = isFollowUp() ? self.cvdPredict(false) : self.cvdPredict(true);
        var optimalBaseline = self.optimalCvdPredict(false);
        var bp = isFollowUp() ? BaselineBloodPressure() : BloodPressure();
        var diabetic = isFollowUp() ? BaselineDiabetic() : Diabetic();

        if(baselineRisk < 0.05 || (bp < 120 || (diabetic == 'Yes' && bp < 130))){
            return 'NA';
        }else{
            return Math.max(baselineRisk * self.relativeRiskStatinBP, optimalBaseline);
        }
    };
    self.ForecastRiskStatinSmoking = function(){
        var baselineRisk = isFollowUp() ? self.cvdPredict(false) : self.cvdPredict(true);
        var optimalBaseline = self.optimalCvdPredict(false);
        var smoke = isFollowUp() ? BaselineSmoker() : Smoker();

        if(baselineRisk < 0.05 || smoke == 'No' || smoke == 'Never'){
            return 'NA';
        }else{
            return Math.max(baselineRisk * self.relativeRiskStatinStopSmoking, optimalBaseline);
        }
    };
    self.ForecastRiskAspirinSmoking = function(){
        var baselineRisk = isFollowUp() ? self.cvdPredict(false) : self.cvdPredict(true);
        var optimalBaseline = self.optimalCvdPredict(false);
        var smoke = isFollowUp() ? BaselineSmoker() : Smoker();

        if(baselineRisk < 0.1 || smoke == 'No' || smoke == 'Never'){
            return 'NA';
        }else{
            return Math.max(baselineRisk * self.relativeRiskAspirinStopSmoking, optimalBaseline);
        }
    };
    self.ForecastRiskBPSmoking = function(){
        var baselineRisk = isFollowUp() ? self.cvdPredict(false) : self.cvdPredict(true);
        var optimalBaseline = self.optimalCvdPredict(false);
        var smoke = isFollowUp() ? BaselineSmoker() : Smoker();
        var bp = isFollowUp() ? BaselineBloodPressure() : BloodPressure();
        var diabetic = isFollowUp() ? BaselineDiabetic() : Diabetic();
        if((bp < 120 || smoke == 'No' || smoke == 'Never') || (diabetic == 'Yes' && bp < 130)) {
            return 'NA';
        }else{
            return Math.max(baselineRisk * self.relativeRiskBPStopSmoking, optimalBaseline);
        }
    };
    self.ForecastRiskAspirinStatinBP = function(){
        var baselineRisk = isFollowUp() ? self.cvdPredict(false) : self.cvdPredict(true);
        var optimalBaseline = self.optimalCvdPredict(false);
        var bp = isFollowUp() ? BaselineBloodPressure() : BloodPressure();
        var diabetic = isFollowUp() ? BaselineDiabetic() : Diabetic();

        if(baselineRisk < 0.1 || (bp < 120 || (diabetic == 'Yes' && bp < 130))){
            return 'NA';
        }else{
            return Math.max(baselineRisk * self.relativeRiskStatinAspirinBP, optimalBaseline);
        }
    };
    self.ForecastRiskAspirinBPSmoking = function(){
        var baselineRisk = isFollowUp() ? self.cvdPredict(false) : self.cvdPredict(true);
        var optimalBaseline = self.optimalCvdPredict(false);
        var smoke = isFollowUp() ? BaselineSmoker() : Smoker();

        var bp = isFollowUp() ? BaselineBloodPressure() : BloodPressure();
        var diabetic = isFollowUp() ? BaselineDiabetic() : Diabetic();

        if(baselineRisk < 0.1 || (bp < 120 || smoke == 'No' || smoke == 'Never') || (diabetic == 'Yes' && bp < 130)) {
            return 'NA';
        }else{
            return Math.max(baselineRisk * self.relativeRiskAspirinBPStopSmoking, optimalBaseline);
        }
    };
    self.ForecastRiskStatinBPSmoking = function(){
        var baselineRisk = isFollowUp() ? self.cvdPredict(false) : self.cvdPredict(true);
        var optimalBaseline = self.optimalCvdPredict(false);
        var smoke = isFollowUp() ? BaselineSmoker() : Smoker();

        var bp = isFollowUp() ? BaselineBloodPressure() : BloodPressure();
        var diabetic = isFollowUp() ? BaselineDiabetic() : Diabetic();

        if(baselineRisk < 0.05 || (bp < 120 || smoke == 'No' || smoke == 'Never') || (diabetic == 'Yes' && bp < 130)) {
            return 'NA';
        }else{
            return Math.max(baselineRisk * self.relativeRiskStatinBPStopSmoking, optimalBaseline);
        }
    };
    self.ForecastRiskAspirinStatinSmoking = function(){
        var baselineRisk = isFollowUp() ? self.cvdPredict(false) : self.cvdPredict(true);
        var optimalBaseline = self.optimalCvdPredict(false);
        var smoke = isFollowUp() ? BaselineSmoker() : Smoker();

        if(baselineRisk < 0.1 || smoke == 'No' || smoke == 'Never'){
            return 'NA';
        }else{
            return Math.max(baselineRisk * self.relativeRiskAspirinStatinStopSmoking, optimalBaseline);
        }
    };
    self.ForecastRiskSartAll4 = function(){
        var baselineRisk = isFollowUp() ? self.cvdPredict(false) : self.cvdPredict(true);
        var optimalBaseline = self.optimalCvdPredict(false);
        var smoke = isFollowUp() ? BaselineSmoker() : Smoker();

        var bp = isFollowUp() ? BaselineBloodPressure() : BloodPressure();
        var diabetic = isFollowUp() ? BaselineDiabetic() : Diabetic();

        if(baselineRisk < 0.1 || (bp < 120 || smoke == 'No' || smoke == 'Never') || (diabetic == 'Yes' && bp < 130)) {
            return 'NA';
        }else{
            return Math.max(baselineRisk * self.relativeRiskAll4, optimalBaseline);
        }
    };
    //end: Forecasted Risk at Initial Visit

    //start: Forecasted Risk at Follow Up Visit
    self.forecasttrlnsbp = function(value) {
        return Math.log(BloodPressure()) * Number(value);
    };

    self.forecastntlnsbp = function(value) {
        return Math.log(BloodPressure()) * Number(!value);
    };

    self.forecastagetsbp = function(value) {
        return self.lnFollowUpage() * self.forecasttrlnsbp(value);
    };

    self.forecastagentsbp = function(value) {
        return self.lnFollowUpage() * self.forecastntlnsbp(value);
    };

    self.forecastagesmoke = function(value) {
        return self.lnFollowUpage() * Number(value);
    };

    self.forecastAspirinDelta = function(value){
        if(value){
            return 0.9;
        }else{
            return 1;
        }
    };

    //Need to check baseline diabetic and smoker values
    self.forecastPredictCalculate = function(isCurrent, bpValue, smokerValue) {
        var i;

        if (isAfrican() && isFemale() )
            i = 17.1141 * (isCurrent ? self.lnFollowUpage(): self.lnage())
                + 0.9396 * self.lntot(isCurrent)
                + (-18.9196 * self.lnhdl(isCurrent))
                + 4.4748 * self.agehdl(isCurrent)
                + 29.2907 * self.forecasttrlnsbp(bpValue)
                + (-6.4321 * self.forecastagetsbp(bpValue))
                + 27.8197 * self.forecastntlnsbp(bpValue)
                + (-6.0873 * self.forecastagentsbp(bpValue))
                + 0.6908 * ( Number(smokerValue))
                + 0.8738 * (isCurrent ? Number(isDiabetic()):Number(isBaseLineDiabetic()));

        if (!isAfrican() && isFemale() )
            i = (-29.799 * (isCurrent ? self.lnFollowUpage(): self.lnage()))
                + 4.884 * self.age2(isCurrent) + 13.54 * self.lntot(isCurrent)
                + (-3.114 * self.agetc(isCurrent))
                + (-13.578 * self.lnhdl(isCurrent))
                + 3.149 * self.agehdl(isCurrent)
                + 2.019 * self.forecasttrlnsbp(bpValue)
                + 1.957 * self.forecastntlnsbp(bpValue)
                + 7.574 * (Number(smokerValue))
                + (-1.665 * self.forecastagesmoke(smokerValue))
                + 0.661 * (isCurrent ? Number(isDiabetic()):Number(isBaseLineDiabetic()));

        if (isAfrican() && isMale())
            i = 2.469 * (isCurrent ? self.lnFollowUpage(): self.lnage())
                + 0.302 * self.lntot(isCurrent)
                + (-0.307 * self.lnhdl(isCurrent))
                + 1.916 * self.forecasttrlnsbp(bpValue)
                + 1.809 * self.forecastntlnsbp(bpValue)
                + 0.549 * (Number(smokerValue))
                + 0.645 * (isCurrent ? Number(isDiabetic()):Number(isBaseLineDiabetic()));

        if (!isAfrican() && isMale())
            i = 12.344 * (isCurrent ? self.lnFollowUpage() : self.lnage())
                + 11.853 * self.lntot(isCurrent)
                + (-2.664 * self.agetc(isCurrent))
                + (-7.99 * self.lnhdl(isCurrent))
                + 1.769 * self.agehdl(isCurrent)
                + 1.797 * self.forecasttrlnsbp(bpValue)
                + 1.764 * self.forecastntlnsbp(bpValue)
                + 7.837 * (Number(smokerValue))
                + (-1.795 * self.forecastagesmoke(smokerValue))
                + 0.658 * (isCurrent ? Number(isDiabetic()) : Number(isBaseLineDiabetic()));

        return i;
    };

    self.forecastCvdPredict = function(isCurrent,bpValue,smokerValue){
        var i;
        i= (1 - Math.pow(self.s010(), Math.exp(self.forecastPredictCalculate(isCurrent,bpValue,smokerValue) - self.mnxb())));
        return i;
    };
    //Forecasted updated Estimates

    self.forecastup_trlnsbp = function(value) {
        return Math.log(BaselineBloodPressure()) * Number(value);
    };
    self.forecastup_ntlnsbp = function(value) {
        return Math.log(BaselineBloodPressure()) * Number(!value);
    };
    self.forecastup_agetsbp = function(value) {
        return self.lnFollowUpage() * self.forecastup_trlnsbp(value);
    };
    //This takes only updated age,bp and smoker and use baseline values
    self.forecastUpdatedPredictCalculate = function(bpValue,smokerValue) {
        var i;
        if (isAfrican() && isFemale() )
            i = 17.1141 * self.lnFollowUpage()
                + 0.9396 * self.lntot(false)
                + (-18.9196 * self.lnhdl(false))
                + 4.4748 * self.agehdl(false)
                + 29.2907 * self.forecastup_trlnsbp(bpValue)
                + (-6.4321 * self.forecastup_agetsbp(bpValue))
                + 27.8197 * self.forecastup_ntlnsbp(bpValue)
                + (-6.0873 * (self.forecastup_ntlnsbp(bpValue) * self.lnFollowUpage()))
                + 0.6908 * Number(smokerValue)
                + 0.8738 * Number(isDiabetic());

        if (!isAfrican() && isFemale() )
            i = (-29.799 * self.lnFollowUpage())
                + 4.884 * self.age2(true)
                + 13.54 * self.lntot(false)
                + (-3.114 * (self.lntot(false) * self.lnFollowUpage()))
                + (-13.578 * self.lnhdl(false))
                + 3.149 * (self.lnhdl(false) * self.lnFollowUpage())
                + 2.019 * self.forecastup_trlnsbp(bpValue)
                + 1.957 * self.forecastup_ntlnsbp(bpValue)
                + 7.574 * Number(smokerValue)
                + (-1.665 * (self.lnFollowUpage() * Number(smokerValue)))
                + 0.661 * Number(isDiabetic());

        if (isAfrican() && isMale())
            i = 2.469 * self.lnFollowUpage()
                + 0.302 * self.lntot(false)
                + (-0.307 * self.lnhdl(false))
                + 1.916 * self.forecastup_trlnsbp(bpValue)
                + 1.809 * self.forecastup_ntlnsbp(bpValue)
                + 0.549 * Number(smokerValue)
                + 0.645 * Number(isDiabetic());

        if (!isAfrican() && isMale())
            i = 12.344 * self.lnFollowUpage()
                + 11.853 * self.lntot(false)
                + (-2.664 * (self.lntot(false) * self.lnFollowUpage()))
                + (-7.99 * self.lnhdl(false))
                + 1.769 * (self.lnhdl(false) * self.lnFollowUpage())
                + 1.797 * self.forecastup_trlnsbp(bpValue)
                + 1.764 * self.forecastup_ntlnsbp(bpValue)
                + 7.837 * Number(smokerValue)
                + (-1.795 * (self.lnFollowUpage() * Number(smokerValue)))
                + 0.658 * Number(isDiabetic());

        if(debug)
            console.log(i);

        return i;
    };

    self.forecastupdatedCvdPredict = function(bpValue,smokerValue) {
        var i;
        i= (1 - Math.pow(self.s010(), Math.exp( self.forecastUpdatedPredictCalculate(bpValue,smokerValue) - self.mnxb())));
        if(debug)
            console.log(i);

        return i;
    };

    self.TenYearForecastedFollowUpRisk = function(isSmoker,isBP,isAspirin){
        var h125 = self.forecastupdatedCvdPredict(isBP,isSmoker)
                * (self.statinDelta()
                * self.bloodPresureDelta()
                * self.smokerDelta()
                * self.forecastAspirinDelta(isAspirin));

        var g59 = self.optimalCvdPredict(true);

        var g92 = self.forecastCvdPredict(true,isBP,isSmoker);

        var number =  Math.min(Math.max(h125,g59), g92) * 100

        return number.toFixed(1) + '%';
    };
}
var formula = new _formula();

