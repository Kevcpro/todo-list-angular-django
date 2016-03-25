angular
    .module("modalController", ['ngAnimate', 'ui.bootstrap'])
    .controller('ModalInstanceCtrl', function ($scope, $uibModalInstance, name) {
        // NOTE $uibModalInstance dependencies
        // define display of modal content and return value
        $scope.DeleteTaskName = name;
        $scope.ok = function () {
            $uibModalInstance.close(true);// NOTE pass to modalResult
        };
        $scope.cancel = function () {
            $uibModalInstance.dismiss(false);// NOTE pass to modalResultReject
        };
});
