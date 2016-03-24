var app = angular.module("app", []);
//create a module with no other dependencies(empty list)
// name of module is myApp, will be registered in html

// define controller: how data is processed from model to view
app.controller("todoController", function($scope, $http){  // attribute must name as $scope

    // tasks groups ng model
    $scope.tasksDone = [];
    $scope.tasksUndone = [];
    //response data model
    $scope.getRespTxt = '';
    $scope.respTxt = '';

    $scope.onClickAddTask = function(taskName){
        // prepare request url and data
        var url = '/todos/';
        //var url = window.location.origin + '/todos/new/'; //redundant
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
                    //
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
        var default_url = window.location.origin + '/todos/';
        url = typeof url !== 'undefined' ? url : default_url;

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
        var url = window.location.origin + '/todos/' + taskID + '/';

        // parse request data
        var data = {};
        if(task.status !== 'undefined'){
            data['status'] = task.status;
        }
        if(task.task !== 'undefined'){
            data['task'] = task.task;
        }

        $http.put(url, data).then(
            function(response){
                console.log('successPUT');
                if (response.status === 200){
                    _sendGetUpdateAngModel();
                    $scope.respTxt = response.data;
                }
            }, function(response){
                console.log('errorPUT');
                _sendGetUpdateAngModel();
            });
    };

    $scope.onClickDeleteTask = function(taskID){
        console.info('task ', taskID, ' is gonna be deleted');
        var url = window.location.origin + '/todos/' + taskID + '/';

        $http.delete(url).then(
            function(response){
                console.log('successDELETE');
                if (response.status === 200){
                    _sendGetUpdateAngModel();
                    $scope.respTxt = response.data;
                }
            }, function(response){
                console.log('errorDELETE');
            });
    };

    // execute when page is loaded
    $scope.init = function(){
        _sendGetUpdateAngModel();
    };

});
