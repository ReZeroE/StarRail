# SPDX-License-Identifier: MIT
# MIT License
#
# Copyright (c) 2023 Kevin L.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import cv2
import time
import numpy as np

class StarRailImageMatcher:
    def __init__(self):
        pass

    def match_image(self, template, screenshot, visualize_match=False, override_threshold=None, secondary_template=None):
        vis, M, coords, dst = self.match_image_base(template, screenshot, visualize_match, override_threshold)
        if secondary_template == None:
            return vis, M, coords
        else:
            try:
                masked_screenshot = self.mask_unmatched_space(cv2.imread(screenshot, cv2.IMREAD_GRAYSCALE), dst)
                vis, M, coords, dst = self.match_image_base(secondary_template, masked_screenshot, visualize_match, override_threshold)
                return vis, M, coords
            except Exception as ex:
                print(ex.args)
                time.sleep(10)


    def match_image_base(self, template, screenshot, visualize_match=False, override_threshold=None):
        """
        SIFT (Scale Invariant Feature Transform) algorithm for feature detection and description, and FLANN (Fast Library for Approximate Nearest Neighbors) for feature matching. 
        The algorithm also uses RANSAC for finding homography to account for any scale, rotation or translation between the images.
        
        :param template: absolute path to the template image
        :param screenshot: absolute path to the screenshot image
        :show_match: generate a visualization for the match. Defaulted to False for optimization. 
        """
        
        if isinstance(template, str):
            img1 = cv2.imread(template, cv2.IMREAD_GRAYSCALE)
        else: img1 = template
        
        if isinstance(screenshot, str):
            img2 = cv2.imread(screenshot, cv2.IMREAD_GRAYSCALE)
        else: img2 = screenshot
        
        MATCH_THRESHOLD = 50 if not isinstance(override_threshold, int) else override_threshold
        MATCH_THRESHOLD = self.downscale_match_threshold(img2, MATCH_THRESHOLD)

        # Initialize SIFT detector
        sift = cv2.SIFT_create()

        # Detect SIFT features in both images
        keypoints1, descriptors1 = sift.detectAndCompute(img1, None)
        keypoints2, descriptors2 = sift.detectAndCompute(img2, None)

        # Initialize FLANN matcher
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=7)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)

        # Match features between the template and screenshot
        matches = flann.knnMatch(descriptors1, descriptors2, k=2)

        # Store all good matches as per Lowe's ratio test
        good = []
        for m, n in matches:
            if m.distance < 0.60 * n.distance:
                good.append(m)

        # print(len(good))
        if len(good) >= MATCH_THRESHOLD:
            print("Good matches are found - %d/%d" % (len(good), MATCH_THRESHOLD))
            src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

            # Compute Homography with RANSAC
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

            # Apply the Homography to transform the corners of template to find corresponding region in the screenshot
            h, w = img1.shape
            pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)

            # Compute the center of the matched region
            center_x = np.mean(dst[..., 0])
            center_y = np.mean(dst[..., 1])

            img2_with_box = None
            if visualize_match == True: # Show template match on screenshot
                # Draw a red rectangle around the detected region in screenshot
                img2_color = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)  # Convert to colored image for visualization
                img2_with_box = cv2.polylines(img2_color, [np.int32(dst)], True, (0, 0, 255), 3, cv2.LINE_AA)
                
                cv2.imshow("visualization with Box", self.mask_unmatched_space(img2_with_box, dst))
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            return None, M, (center_x, center_y), dst

        else:
            print("Not enough matches are found - %d/%d" % (len(good), MATCH_THRESHOLD))
            return None, None, None, None
        

    def downscale_match_threshold(self, screenshot, curr_threshold):
        """
        Downscale feature matching threshold based on the screen resolution.
        
        NOTE: The user MUST set the in-game resolution to the native screen resolution or higher. 
            Lower in-game resolution (incorrect threshold downscale) may lead to false positives in feature matches.
            
         - 4K       => * 1.0
         - 2K       => * 0.8
         - 1080P    => * 0.6
         - Other    => * 0.4
         
         :param screenshot: The screenshot image
         :curr_threshold: The original threshold to downscale
        """
        if isinstance(screenshot, None.__class__):
            return curr_threshold
        
        def get_image_resolution(screenshot: cv2.Mat):
            height, width = screenshot.shape
            return height, width
        
        height, width = get_image_resolution(screenshot)
        if width >= 3840 and height >= 2160:
            return curr_threshold
        elif width >= 2560 and height >= 1200:
            curr_threshold = curr_threshold * 0.8
        elif width >= 1920 and height >= 1080:
            curr_threshold = curr_threshold * 0.6
        else:
            curr_threshold = curr_threshold * 0.4
            
        if curr_threshold < 1: curr_threshold = 1
        print(f"downgraded threshold {curr_threshold}")
        return int(curr_threshold)

    def mask_unmatched_space(self, original_img, dst):
        # Fill the ROI into the mask
        mask = np.zeros_like(original_img)
        cv2.fillPoly(mask, [np.int32(dst)], (255, 255, 255))
        
        # Performing bitwise and operation with mask image
        result = cv2.bitwise_and(original_img, mask)
        return result


# if __name__ == "__main__":
#     import os
#     image_detector = StarRailImageMatcher()

#     TEMPLATE                    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp_data", "template.PNG")
#     ORIGINAL                    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp_data", "original.PNG")
#     ORIGINAL_2                  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp_data", "original-2.png")
#     ORIGINAL_ORIENTED           = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp_data", "original-oriented.jpg")
#     ORIGINAL_COMPRESSED         = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp_data", "original-compressed.jpg")
#     ORIGINAL_DOUBLE_COMPRESSED  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp_data", "original-double-compressed.jpg")

#     SC_with_box, M, center = image_detector.match_image(TEMPLATE, ORIGINAL, visualize_match=True, override_threshold=25)

#     if M is not None:
#         cv2.imshow("visualization with Box", SC_with_box)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()