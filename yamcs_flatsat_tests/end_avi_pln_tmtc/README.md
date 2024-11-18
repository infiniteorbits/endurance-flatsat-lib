### README - Test Procedures for TMTC Routing

#### Overview
This README provides detailed information on the test procedures TMTC_ROU_01 to TMTC_ROU_04. These procedures are designed to validate various aspects of Telemetry and Telecommand (TMTC) routing and handling within the onboard computers (OBCs) of the system. Each test case focuses on a specific aspect of TMTC functionality, such as routing, handling of high traffic, and error handling.

---

### TMTC_ROU_01 - General Routing Validation

**Objective**:
To validate the correct routing of TCs and TMs across active and standby OBCs for Mission, ADCS, and GNC subsystems.

**Test Steps**:
1. **Test Setup Configuration**
   - Initial configuration of the test environment.

2. **Send TC[17,1] to Active and Standby OBCs**
   - TCs are sent to the Active Mission OBC, Standby Mission OBC, Active ADCS OBC, Standby ADCS OBC, Active GNC OBC, and Standby GNC OBC.
   - Expected Results: TM[1,1], TM[1,7], and TM[17,2] should be received from each.

3. **Check Counter Increments**
   - Verify that the accepted TC counters on the OBCs are incremented.
   - Verify that forwarded TC counters on the Active Mission OBC are incremented.
   - Verify that the sent TM counter on the active OBC is incremented.

4. **Reset and Retrieve Counters**
   - Reset TC counters and verify they reset correctly.
   - Send TC to retrieve deferred telemetry and ensure correct TM[1,1], TM[1,7], and TM[17,2] are received in order.

5. **End Test and Reset Configuration**

**Expected Results**:
All TCs should be routed correctly with corresponding telemetry being received. All counters should increment and reset as expected.

---

### TMTC_ROU_02 - Force Standby TM Mode

**Objective**:
To demonstrate that TMs are routed directly from the standby OBC to the radio when the active OBC is non-responsive, and that the system can handle forced mode configurations.

**Test Steps**:
1. **Test Setup Configuration**
   - Initial configuration of the test environment.

2. **Disable Active OBC Keep-Alive**
   - This simulates the failure of the active OBC and forces the system to switch CAN bus.

3. **Set Standby OBC in "TM Forced Mode"**
   - Send TCs to configure the standby OBC in TM Forced Mode.
   - Expected Results: TM[1,1] and TM[1,7] should be received.

4. **Send TC[17,1] to Standby OBCs**
   - Verify that TMs are received from standby Mission and ADCS OBCs.

5. **Check Counter Increments on Standby OBC**
   - Verify that the accepted TC, forwarded TC, and sent TM counters on the standby OBC increment correctly.

6. **Reset and Restore Configuration**
   - Reset all counters and restore keep-alive messages to their original state.

7. **End Test and Reset Configuration**

**Expected Results**:
The standby OBC should correctly take over TM routing, with appropriate counter increments and telemetry generation.

---

### TMTC_ROU_03 - Housekeeping (HK) Routing Under Load

**Objective**:
To demonstrate the system's capability to handle high levels of housekeeping TM traffic, maintaining a throughput of more than 50 TM/s.

**Test Steps**:
1. **Test Setup Configuration**
   - Initial configuration of the test environment.

2. **Define and Configure HK Parameters**
   - Set up the OBCs with HK parameters to generate full HK TMs.

3. **Configure HK Generation for High Traffic**
   - Set the system to generate 50 HK TMs per second.

4. **Enable Active Radio**
   - Verify that TM[3,25] is sent periodically to the ground.

5. **Monitor TM Traffic**
   - Check that the system is maintaining a rate of more than 50 TM/s.

6. **End Test and Reset Configuration**

**Expected Results**:
The system should maintain a consistent TM throughput of more than 50 TM/s under high-load conditions.

---

### TMTC_ROU_04 - Break Routing Chain

**Objective**:
To evaluate the system's robustness by testing its behavior with incorrect or incomplete TCs and to determine the maximum TC/s the OBC can handle.

**Test Steps**:
1. **Test Setup Configuration**
   - Initial configuration of the test environment.

2. **Set Discarded TCs as a Housekeeping Parameter**
   - Ensure discarded TCs are monitored.

3. **Bypass Radio and Connect Directly to CAN-TS**
   - This simulates a radio failure.

4. **Send Incomplete or Incorrect TCs**
   - Send partial TCs, TCs with incorrect signatures, structures, or non-assigned APIDs to both active and standby OBCs.
   - Expected Results: Appropriate error telemetry (e.g., TM[1,2], TM[5,2], TM[1,10]) should be generated.

5. **Check Discarded TC Counters**
   - Verify the counters for discarded TCs on both active and standby OBCs.

6. **Stress Test with High TC Rate**
   - Send more than 10 full TCs per second and monitor the system's response.

7. **End Test and Reset Configuration**

**Expected Results**:
The OBC should handle incorrect TCs appropriately by generating error telemetry and discarding them. The system should be capable of handling a high rate of TC input.

---

### Final Notes
- **Test Data**: Throughout the tests, specific counter values and telemetry formats are marked as "TBD" and should be determined during the actual test execution.
- **Reset Procedures**: Each test case ends with resetting the test environment to ensure no residual configuration impacts subsequent tests.
- **Expected Results**: All expected results are based on standard TM/TC handling and routing protocols. Any deviation should be thoroughly investigated.