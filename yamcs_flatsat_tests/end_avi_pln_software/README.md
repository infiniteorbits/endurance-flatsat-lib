### README - Test Procedures for Boot Software (BSW) Validation

#### Overview
This README provides details on the test procedures BSW_BOOT_01 and BSW_BOOT_02. These procedures are designed to validate the boot process of the Onboard Computer (OBC) when uploading and managing software images. BSW_BOOT_01 focuses on the standard boot process, while BSW_BOOT_02 is designed to test the system's response to a corrupted software image.

---

### BSW_BOOT_01 - Standard Boot Process

**Objective**:
To validate the correct loading and verification of a software image on the OBC through a standard boot process.

**Test Steps**:

1. **Upload SW Image on OBC**
   - **Test Data**: Link to the zipped SW image to upload.
   - **Expected Result**: The functional image is stored in a known memory address on slot 1.

2. **Set Next Boot Image to Slot 1**
   - **Test Data**: None.
   - **Expected Result**: The OBC is configured to load the image from slot 1 during the next boot.

3. **Power Cycle the OBC**
   - **Test Data**: None.
   - **Expected Result**: The new SW image from slot 1 loads successfully.

4. **Wait for the SW Application to Send its Heartbeat**
   - **Test Data**: None.
   - **Expected Result**: The SW application starts running, indicated by the heartbeat signal.

5. **Check Image Loaded and Image Verification**
   - **Test Data**: None.
   - **Expected Result**: The image in slot 1 is loaded, the next image to load is determined (TBD), and the checksum should match the expected value.

6. **Download the Boot Report**
   - **Test Data**: None.
   - **Expected Result**: The boot report is successfully downloaded.

7. **Verify Boot Report**
   - **Test Data**: None.
   - **Expected Result**: All steps in the boot process (HW checks, initialization of volatile memory, SW image loading, SW image integrity check, and SW image execution) pass successfully.

---

### BSW_BOOT_02 - Break Boot Process

**Objective**:
To test the OBC's ability to handle a corrupted software image by verifying the fallback to a functional image stored in a different slot.

**Test Steps**:

1. **Upload Corrupted SW Image on OBC**
   - **Test Data**: Link to the corrupted SW image to upload.
   - **Expected Result**: The corrupted image is stored in a known memory address on slot 1.

2. **Upload Working SW Image on OBC**
   - **Test Data**: Link to the zipped SW image to upload.
   - **Expected Result**: The functional image is stored in a known memory address on slot 2.

3. **Set Next Boot Image to Slot 1**
   - **Test Data**: None.
   - **Expected Result**: The OBC is configured to attempt loading the image from slot 1 during the next boot.

4. **Power Cycle the OBC**
   - **Test Data**: None.
   - **Expected Result**: The OBC fails to load the corrupted image in slot 1 and successfully loads the image from slot 2.

5. **Wait for the SW Application to Send its Heartbeat**
   - **Test Data**: None.
   - **Expected Result**: The SW application starts running from the image in slot 2, indicated by the heartbeat signal.

6. **Check Image Loaded and Image Verification**
   - **Test Data**: None.
   - **Expected Result**: The image in slot 2 is loaded, the next image to load is determined (TBD), and the checksum should match the expected value.

7. **Download the Boot Report**
   - **Test Data**: None.
   - **Expected Result**: The boot report is successfully downloaded.

8. **Verify Boot Report**
   - **Test Data**: None.
   - **Expected Result**: The corrupted image in slot 1 fails to load during the integrity check step, and the OBC successfully loads the image from slot 2. The report should confirm the initialization of volatile memory, SW image loading, integrity check, and SW image execution.

---

### Final Notes
- **Test Data**: Links to the zipped SW images (both functional and corrupted) should be prepared before the test execution.
- **Reset Procedures**: Ensure the OBC is reset to a known good state after testing to avoid impact on subsequent tests.
- **Expected Results**: All expected results are based on standard boot processes. Any deviations should be investigated and documented.