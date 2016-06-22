"""
Canvas format templates.
"""

MANIFEST = u'''<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="manifest" xmlns="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1" xmlns:lom="http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource" xmlns:lomimscc="http://ltsc.ieee.org/xsd/imsccv1p1/LOM/manifest" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1 http://www.imsglobal.org/profile/cc/ccv1p1/ccv1p1_imscp_v1p2_v1p0.xsd http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource http://www.imsglobal.org/profile/cc/ccv1p1/LOM/ccv1p1_lomresource_v1p0.xsd http://ltsc.ieee.org/xsd/imsccv1p1/LOM/manifest http://www.imsglobal.org/profile/cc/ccv1p1/LOM/ccv1p1_lommanifest_v1p0.xsd">
  <metadata>
    <schema>IMS Common Cartridge</schema>
    <schemaversion>1.1.0</schemaversion>
    <lomimscc:lom>
      <lomimscc:general>
        <lomimscc:title>
          <lomimscc:string>{course_name}</lomimscc:string>
        </lomimscc:title>
      </lomimscc:general>
      <lomimscc:lifeCycle>
        <lomimscc:contribute>
          <lomimscc:date>
            <lomimscc:dateTime/>
          </lomimscc:date>
        </lomimscc:contribute>
      </lomimscc:lifeCycle>
      <lomimscc:rights>
        <lomimscc:copyrightAndOtherRestrictions>
          <lomimscc:value>yes</lomimscc:value>
        </lomimscc:copyrightAndOtherRestrictions>
        <lomimscc:description>
          <lomimscc:string/>
        </lomimscc:description>
      </lomimscc:rights>
    </lomimscc:lom>
  </metadata>
  <organizations>
    <organization identifier="org_1" structure="rooted-hierarchy">
      <item identifier="LearningModules"/>
    </organization>
  </organizations>
  <resources>
    <resource identifier="syllabus" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="course_settings/syllabus.html" intendeduse="syllabus"/>
    <resource identifier="settings" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="course_settings/canvas_export.txt"/>{resources}
  </resources>
</manifest>'''

RESOURCE = u'''
    <resource identifier="{}" type="{}" href="{}">
      <file href="{}" />
    </resource>'''

WIKI = u'''<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>{}</title>
<meta name="identifier" content="{}"/>
<meta name="editing_roles" content="teachers"/>
<meta name="workflow_state" content="unpublished"/>
</head>
<body>
{}
</body>
</html>'''

QUIZ_METADATA = u'''<?xml version="1.0" encoding="UTF-8"?>
<quiz identifier="{quiz_id}" xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 http://canvas.instructure.com/xsd/cccv1p0.xsd">
  <title><![CDATA[{title}]]></title>
  <description><![CDATA[{preamble}]]></description>
  <shuffle_answers>{shuffle}</shuffle_answers>
  <scoring_policy>keep_highest</scoring_policy>
  <quiz_type>{quiz_type}</quiz_type>
  <points_possible>{points}</points_possible>
  <lockdown_browser_monitor_data/>
  <show_correct_answers>{show_answer}</show_correct_answers>
  <anonymous_submissions>false</anonymous_submissions>
  <allowed_attempts>{attempts}</allowed_attempts>
  <one_question_at_a_time>false</one_question_at_a_time>
  <cant_go_back>false</cant_go_back>
  <available>false</available>
  <one_time_results>false</one_time_results>
  <show_correct_answers_last_attempt>false</show_correct_answers_last_attempt>
</quiz>'''

QUIZ_DATA = u'''<?xml version="1.0" encoding="UTF-8"?>
<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd">
  <assessment ident="{quiz_id}" title="{title}">
    <qtimetadata></qtimetadata>
    <section ident="root_section">{question_groups}
    </section>
  </assessment>
</questestinterop>'''

QUESTION_GROUP = u'''
      <section ident="{group_id}" title="{group_title}">
        <selection_ordering>
          <selection>
            <selection_number>{num_select}</selection_number>
            <selection_extension>
              <points_per_item></points_per_item>
            </selection_extension>
          </selection>
        </selection_ordering>{questions}
      </section>'''

QUESTION = u'''
        <item ident="{question_id}" title="{question_title}">
          <itemmetadata>
            <qtimetadata>
              <qtimetadatafield>
                <fieldlabel>question_type</fieldlabel>
                <fieldentry>{question_type}</fieldentry>
              </qtimetadatafield>
              <qtimetadatafield>
                <fieldlabel>points_possible</fieldlabel>
                <fieldentry>{question_points}</fieldentry>
              </qtimetadatafield>
            </qtimetadata>
          </itemmetadata>{presentation}{processing}{feedback}
        </item>'''

PRESENTATION = u'''
          <presentation>
            <material>
              <mattext texttype="text/html"><![CDATA[{question_text}]]></mattext>
            </material>{options_text}
          </presentation>'''

OPTIONS_NUMERICAL = u'''
            <response_str ident="response1" rcardinality="Single">
              <render_fib fibtype="Decimal">
                <response_label ident="answer1"/>
              </render_fib>
            </response_str>'''

OPTIONS_SHORT = u'''
            <response_str ident="response1" rcardinality="Single">
              <render_fib>
                <response_label ident="answer1" rshuffle="No"/>
              </render_fib>
            </response_str>'''

OPTIONS_SINGLE = u'''
            <response_lid ident="response1" rcardinality="Single">
              <render_choice>{options}
              </render_choice>
            </response_lid>'''

OPTIONS_MULTIPLE = u'''
            <response_lid ident="response1" rcardinality="Multiple">
              <render_choice>{options}
              </render_choice>
            </response_lid>'''

OPTION = u'''
                <response_label ident="{option_id}">
                  <material>
                    <mattext texttype="text/html"><![CDATA[{option_text}]]></mattext>
                  </material>
                </response_label>'''

PROCESSING = u'''
          <resprocessing>
            <outcomes>
              <decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/>
            </outcomes>{feedback}{answer}
          </resprocessing>'''

PROCESSING_FEEDBACK = u'''
            <respcondition continue="Yes">
              <conditionvar>{condition}
              </conditionvar>
              <displayfeedback feedbacktype="Response" linkrefid="{option_id}_fb"/>
            </respcondition>'''

PROCESSING_ANSWER = u'''
            <respcondition continue="No">
              <conditionvar>{condition}
              </conditionvar>
              <setvar action="Set" varname="SCORE">100</setvar>
            </respcondition>'''

PROCESSING_ANSWER_TEXT = u'''
            <respcondition continue="No">
              <conditionvar>{condition}
              </conditionvar>
              <setvar action="Set" varname="SCORE">100</setvar>
              <displayfeedback feedbacktype="Response" linkrefid="{option_id}"/>
            </respcondition>'''

CONDITION_OTHER = u'''
                <other/>'''

CONDITION_EQUAL = u'''
                <varequal respident="response1"><![CDATA[{}]]></varequal>'''

CONDITION_EXACT = u'''
                <or>
                  <varequal respident="response1">{0}</varequal>
                  <and>
                    <vargte respident="response1">{0}</vargte>
                    <varlte respident="response1">{0}</varlte>
                  </and>
                </or>'''

CONDITION_RANGE = u'''
                <vargte respident="response1">{0}</vargte>
                <varlte respident="response1">{1}</varlte>'''

CONDITION_MULTIPLE = u'''
                <and>{}
                </and>'''

CONDITION_MULTIPLE_CORRECT = u'''
                  <varequal respident="response1">{}</varequal>'''

CONDITION_MULTIPLE_INCORRECT = u'''
                  <not>
                    <varequal respident="response1">{}</varequal>
                  </not>'''

FEEDBACK = u'''
          <itemfeedback ident="{option_id}_fb">
            <flow_mat>
              <material>
                <mattext texttype="text/html"><![CDATA[{option_feedback}]]></mattext>
              </material>
            </flow_mat>
          </itemfeedback>'''
