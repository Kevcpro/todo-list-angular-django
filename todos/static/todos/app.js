var app = angular.module("app", ['ngAnimate', 'ui.bootstrap']);
//create a module with no other dependencies(empty list)
// name of module is myApp, will be registered in html

// define controller: how data is processed from model to view
app.controller("todoController", function($scope, $http, $uibModal, $log){  // attribute must name as $scope

    // tasks groups ng model
    $scope.tasksDone = [];
    $scope.tasksUndone = [];
    //response data model
    //$scope.getRespTxt = '';
    //$scope.respTxt = '';
    $scope.alerts = []; // alert message

    $scope.addAlert = function(text) {
        $scope.alerts.splice(0, 0, {msg: text}); // insert
        // splice(pos, removedNums, [elements, ])
    };
    $scope.closeAlert = function(index) {
        $scope.alerts.splice(index, 1); // remove one
    };

    $scope.onClickAddTask = function(taskName){
        // prepare request url and data
        var url = '/todos/';
        var data = {'task':taskName};

        $http.post(url, data).then(
            function(response){
                console.log('successPOST');
                if (response.status === 201){
                    _sendGetUpdateAngModel();
                    $scope.newTaskName = '';                   // clear input
                    $scope.respTxt = response.data;
                    // NOTE: cannot clear $scope.getRespTxt here
                    $scope.getRespTxt = '';  // invalid
                    console.log($scope.getRespTxt);
                    $scope.addAlert(response.data.result);
                }
            }, function(response){
                // handle task limit condition
                if (response.status === 403){
                    $scope.respTxt = response.data;
                    alert('reach 30 tasks limit');
                }
                console.log('errorPOST');
            });
    };

    function _updateTaskAngModel(response){
        // group tasks by status, update ng model and view
        $scope.tasksDone = [];
        $scope.tasksUndone = [];
        var respData = response.data.data;
        var task;
        for (var index in respData){
            task = respData[index];
            if (task.status === true){
                $scope.tasksDone.push(task);
            } else{
                $scope.tasksUndone.push(task);
            }
        }
    }

    function _sendGetUpdateAngModel(url){
        // get current host and port
        url = url || '/todos/';

        $http.get(url).then(
            function(response){
                $scope.getRespTxt = response.data.data;  // type object
                _updateTaskAngModel(response);
                console.log('successGET');
            }, function(response){
                console.log('errorGET');
            });
    }

    // change task status
    $scope.onClickUpdateTask = function(taskID, task){
        console.info('task', taskID, ' is gonna update to status ', task.status);
        console.info('task', taskID, ' is gonna update to name ', task.task);

        // prepare request url and data
        var url = '/todos/' + taskID + '/';

        // parse request data
        var data = {};
        if(task.status !== 'undefined'){
            data.status = task.status;
        }
        if(task.task !== 'undefined'){
            data.task = task.task;
        }

        $http.put(url, data).then(
            function(response){
                console.log('successPUT');
                if (response.status === 200){
                    _sendGetUpdateAngModel();
                    $scope.respTxt = response.data;
                    $scope.addAlert(response.data.result);
                }
            }, function(response){
                console.log('errorPUT');
                _sendGetUpdateAngModel();
            });
    };

    $scope.onClickDeleteTask = function(taskID, taskName){
        console.info('task ', taskID, ' is gonna be deleted');
        var url = '/todos/' + taskID + '/';

        // confirm modal
        var modalInstance = $uibModal.open({
            animation: true,
            templateUrl: 'my_modal_id',
            controller: 'ModalInstanceCtrl',
            size: 'lg',
            resolve: {  // Members that will be resolved and passed to the modal controller as locals
                name: function () {
                    return taskName;
                }
            }
        });

        // NOTE callback
        modalInstance.result.then(function (modalResult) {
            // NOTE resolve function
            $log.info('Modal confirmed at: ' + new Date() + ' ' + modalResult);

            // NOTE OLD http delete call
            $http.delete(url).then(
                function(response){
                    console.log('successDELETE');
                    if (response.status === 200){
                        _sendGetUpdateAngModel();
                        $scope.respTxt = response.data;
                        $scope.addAlert(response.data.result + ' : ' + taskName );
                    }
                }, function(response){
                    console.log('errorDELETE');
                });

        }, function (modalResultReject) {
            // NOTE reject function
            $log.info('Modal dismissed at: ' + new Date() + ' ' + modalResultReject);
            }
        );

    };

    // execute when page is loaded
    $scope.init = function(){
        _sendGetUpdateAngModel();
    };

});

app.controller('ModalInstanceCtrl', function ($scope, $uibModalInstance, name) {
    // define display of modal content and return value
    $scope.DeleteTaskName = name;
    $scope.ok = function () {
        $uibModalInstance.close(true);// NOTE pass to modalResult
    };
    $scope.cancel = function () {
        $uibModalInstance.dismiss(false);// NOTE pass to modalResultReject
    };
});
