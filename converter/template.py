"""
Canvas format templates.
"""

QUIZ_META = u'''<?xml version="1.0" encoding="UTF-8"?>
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
          </itemmetadata>
          <presentation>
            <material>
              <mattext texttype="text/html"><![CDATA[{question_text}]]></mattext>
            </material>{options}
          </presentation>{feedback}
        </item>'''

OPTION_GROUP_TEXT = u'''
            <response_str ident="response1" rcardinality="Single">
              <render_fib {fibtype}>
                <response_label ident="answer1" rshuffle="No"/>
              </render_fib>
            </response_str>'''

OPTION_GROUP_CHOICE = u'''
            <response_lid ident="response1" rcardinality="{single}">
              <render_choice>{options}
              </render_choice>
            </response_lid>'''

OPTION = u'''
                <response_label ident="{option_id}">
                  <material>
                    <mattext texttype="text/html"><![CDATA[{option_text}]]></mattext>
                  </material>
                </response_label>'''

FEEDBACK = u'''
          <itemfeedback ident="{option_id}_fb">
            <flow_mat>
              <material>
                <mattext texttype="text/html"><![CDATA[{option_feedback}]]></mattext>
              </material>
            </flow_mat>
          </itemfeedback>'''
