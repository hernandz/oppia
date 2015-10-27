// Copyright 2014 The Oppia Authors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS-IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/**
 * Directive for the PencilCodeEditor interaction.
 *
 * IMPORTANT NOTE: The naming convention for customization args that are passed
 * into the directive is: the name of the parameter, followed by 'With',
 * followed by the name of the arg.
 */
oppia.directive('oppiaInteractivePencilCodeEditor', [
  'oppiaHtmlEscaper', function(oppiaHtmlEscaper) {
    return {
      restrict: 'E',
      scope: {},
      templateUrl: 'interaction/PencilCodeEditor',
      controller: ['$scope', '$attrs', '$element', '$timeout', 'focusService',
          function($scope, $attrs, $element, $timeout, focusService) {

        $scope.initialCode = oppiaHtmlEscaper.escapedJsonToObj(
          $attrs.initialCodeWithValue);

        var pce = new PencilCodeEmbed($element[0].children[0]);
        pce.beginLoad($scope.initialCode);
        pce.on('load', function() {
          // Hide the turtle, and redefine say() to also write the text on the
          // screen.
          pce.setupScript([{
            code: [
              'ht();',
              '',
              'oldsay = window.say',
              'say = function(x) {',
              '  write(x);',
              '  oldsay(x);',
              '};'
            ].join('\n'),
            type: 'text/javascript'
          }]);

          pce.hideToggleButton();
          pce.setEditable();
          pce.showEditor();

          // Pencil Code automatically takes the focus on load, so we clear it.
          focusService.clearFocus();
        });

        $scope.reset = function() {
          pce.setCode($scope.initialCode);
        };

        var errorIsHappening = false;
        var hasSubmittedAnswer = false;

        pce.on('startExecute', function() {
          hasSubmittedAnswer = false;

          // If no answer has been submitted within 3 seconds, submit just the
          // code to the backend.
          $timeout(function() {
            if (!hasSubmittedAnswer) {
              console.log('Code: ');
              console.log(pce.getCode());
              console.log('No output received; submitting before run finished.');
              console.log('------');

              hasSubmittedAnswer = true;
              $scope.$parent.$parent.submitAnswer({
                code: pce.getCode(),
                output: '',
                evaluation: '',
                error: ''
              });
            }
          }, 3000);
        });

        pce.on('execute', function() {
          if (errorIsHappening || hasSubmittedAnswer) {
            return;
          }

          // TODO(sll): Separate console output lines by newline characters.
          pce.eval("$('body div').text();", function(output) {
            console.log('Code: ');
            console.log(pce.getCode());
            console.log('Output: ');
            console.log(output);
            console.log('------');

            hasSubmittedAnswer = true;
            $scope.$parent.$parent.submitAnswer({
              code: pce.getCode(),
              output: output || '',
              evaluation: '',
              error: ''
            });
          });
        });

        pce.on('error', function(error) {
          if (hasSubmittedAnswer) {
            return;
          }

          console.log('Code: ');
          console.log(pce.getCode());
          console.log('Error: ');
          console.log(error.message);
          console.log('------');

          errorIsHappening = true;
          hasSubmittedAnswer = true;

          $scope.$parent.$parent.submitAnswer({
            code: pce.getCode(),
            output: '',
            evaluation: '',
            error: error.message
          });

          $timeout(function() {
            errorIsHappening = false;
          }, 1000);
        });
      }]
    };
  }
]);

oppia.directive('oppiaResponsePencilCodeEditor', [
  'oppiaHtmlEscaper', function(oppiaHtmlEscaper) {
    return {
      restrict: 'E',
      scope: {},
      templateUrl: 'response/PencilCodeEditor',
      controller: ['$scope', '$attrs', function($scope, $attrs) {
        $scope.answerCode = oppiaHtmlEscaper.escapedJsonToObj($attrs.answer).code;
      }]
    };
  }
]);

oppia.directive('oppiaShortResponsePencilCodeEditor', [
  'oppiaHtmlEscaper', function(oppiaHtmlEscaper) {
    return {
      restrict: 'E',
      scope: {},
      templateUrl: 'shortResponse/PencilCodeEditor',
      controller: ['$scope', '$attrs', function($scope, $attrs) {
        $scope.answerCode = oppiaHtmlEscaper.escapedJsonToObj($attrs.answer).code;
      }]
    };
  }
]);
