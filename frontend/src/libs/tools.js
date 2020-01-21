export default (function() {
    return {
        getBaseLog: function (x, y) {
            return Math.log(y) / Math.log(x);
        },
        volumeInterpolation: function(x) {
            let output = -this.getBaseLog(28, -(x - 1.04) );
            if(output > 1) {
                console.log(output);
                output = 1;
            } else if(output < 0) {
                console.log(output);
                output = 0;
            }
            return output;
        }
    };
})();
