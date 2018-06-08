# -*- coding: utf-8 -*-
"""
Created on Thu Dec 9 2017

@author: hintenan
"""

## 2016/8/14 Try to modulate everything
import RPi.GPIO as GPIO
import numpy as np
import pygame, time, random, math, csv
from rc import rc_time, uwater


# record current time 
localtime = time.asctime( time.localtime(time.time()) )
initiate_time = time.time()

#open a data file
print "If sound dose not work properly, input \"amixer cset numid=3 1\" in command line."
fm = raw_input("File name: ")
f = open("Fan_data/" + fm + ".csv", "a+")
w = csv.writer(f)


# set GPIO parameters
GPIO.setmode(GPIO.BOARD)
pin_to_infra_left = 11
pin_to_infra_mid = 13
pin_to_infra_right = 15
pin_water_left = 36
pin_water_mid = 38
pin_water_right = 40
GPIO.setup(pin_water_left, GPIO.OUT)
GPIO.setup(pin_water_mid, GPIO.OUT)
GPIO.setup(pin_water_right, GPIO.OUT)
GPIO.output(pin_water_left, False)
GPIO.output(pin_water_mid, False)
GPIO.output(pin_water_right, False)
cho = [11, 15]
wat = [36, 40]
go = ['Go left', 'Go right']

# pygame mixer parameters
pygame.mixer.init()
CS = pygame.mixer.Sound("S3000.wav")
# pygame window parameters
xaxis = 1440.0
yaxis = 900.0
cutoff = 3.0/5
rad = int(round(xaxis/6*cutoff))
bg = 128
background_colour = (bg, bg, bg)
triWidth = xaxis/3

screen = pygame.display.set_mode((int(xaxis), int(yaxis)), 0, 32)
screen.fill(background_colour)
pygame.display.flip()

# some variables
rightLeft = 0
gone = 0
re_gone = 0
tx = [(xaxis-triWidth, yaxis/2, triWidth, triWidth), (0, yaxis/2, triWidth, triWidth), (triWidth, yaxis/2, triWidth, triWidth)]
ty = [(0, 400), (xaxis-triWidth, 400), (triWidth, 400)]
cue_img = pygame.image.load('gabor_mix/sign_gabor.png').convert()
#gra_img = pygame.image.load('tif_col/gabor_new.png').convert()

# permutation pic number
blockd = np.random.permutation([74]) # the grating number
cad = np.random.permutation(['a', 'c', 'a', 'c', 'a', 'c', 'a', 'c', 'a', 'c']) # two kinds of sine wave

# pemutation contrast number
num_contrast = np.random.permutation([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15, 17, 19, 21, 26, 31, 36, 41, 61, 81, 101, 127]) # the contrast level

# pre-trial contrast
pre_contrast = 127

# give a time punishment if wrong
punishment_time = 7

# fix the first sound problem
CS.play()
time.sleep(0.2)
CS.stop()

# memory the choice
fail_rechoice = 0
# memory the correct number
correct_number = 0

# time of water (second)
water_time = 0.015

# end of permutation pic number
sensi = 30
# Initiate program
try:

    print ("Pre-test star!")
    print ("Starting time: " + localtime )
    print ("water valve open time: " + str(water_time) + " second !")
    
    # pre-test
    while True:
        
        # always start in center
        screen.blit(cue_img, (triWidth, 400))
        pygame.display.update()
        zero = time.time()
        

        while True:
            num_gone = gone % 4 # two kinds of sine wave negative of postitive
            num_gone_grating = gone % 1  # how many number it chose from the grating
            num_gone_contrast = gone % 1  # how many number it chose from the contrast
            #sen_gra = 'gabor_mix/gradient' + '4' + cad[num_gone] + '.png'
            sen_gra = 'gabor_mix/contrast' + str(pre_contrast) + 'gradient' + str(blockd[num_gone_grating]) + cad[num_gone] + '.png'
            gra_img = pygame.image.load(sen_gra).convert()

            if  rc_time(pin_to_infra_mid) < sensi:
                # double check module
                if time.time() - zero < 0.5:
                    continue
                elif rc_time(pin_to_infra_mid) > sensi:
                    continue
                elif rc_time(pin_to_infra_mid) > sensi:
                    continue
                elif rc_time(pin_to_infra_mid) > sensi:
                    continue
                elif rc_time(pin_to_infra_mid) > sensi:
                    continue

                first_time = time.time()

                # memory the choice
                if fail_rechoice == 1:
                    print "repeat the same choice:"
                elif fail_rechoice == 0:
                    rightLeft = int(round(random.random()))  # random reight/left
                
                pygame.draw.rect(screen, background_colour, tx[2])
                screen.blit(gra_img, ty[rightLeft])
                pygame.display.update()
                print(go[rightLeft])
                time.sleep(0.05)
                break
        

        while True:
            count1 = rc_time(cho[rightLeft])
            count2 = rc_time(cho[(rightLeft+1)%2])
            if count1 < sensi:
                # double check module
                if time.time()- first_time < 0.5:
                    continue
                elif rc_time(cho[rightLeft]) > sensi:
                    continue
                elif rc_time(cho[rightLeft]) > sensi:
                    continue
                elif rc_time(cho[rightLeft]) > sensi:
                    continue
                elif rc_time(cho[rightLeft]) > sensi:
                    continue
               
                
                second_time = time.time()

                # water module
                # uwater(wat[rightLeft])
                GPIO.output(wat[rightLeft], True)
                time.sleep(water_time)
                GPIO.output(wat[rightLeft], False)

                # data module
                print rightLeft, "Go center"
                data = [gone + 1, 1, second_time - first_time, first_time-zero, rightLeft, rightLeft, str(blockd[num_gone_grating]), cad[num_gone], pre_contrast]
                print data
                #w.writerow(data)
                pygame.draw.rect(screen, background_colour, tx[(rightLeft+1)%2])

                time_elpased = round((second_time - initiate_time)/60, 2)
                if time_elpased >= 60:
                    print ("Time elapsed: " + str(time_elpased) + " minutes!")

                fail_rechoice = 0
                correct_number += 1

                break


            if count2 < sensi:
                # wrong choice, restart trial
                # double check module
                if time.time()- first_time < 0.5:
                    continue
                elif rc_time(cho[(rightLeft+1)%2]) > sensi:
                    continue
                elif rc_time(cho[(rightLeft+1)%2]) > sensi:
                    continue
                elif rc_time(cho[(rightLeft+1)%2]) > sensi:
                    continue
                elif rc_time(cho[(rightLeft+1)%2]) > sensi:
                    continue
                
                second_time= time.time()

                # sound module
                CS.play()
                time.sleep(0.2)
                CS.stop()

                # data module
                print rightLeft, " Wrong but go Center"
                data = [gone + 1, 0, second_time - first_time, first_time-zero, (not rightLeft)*1, rightLeft, str(blockd[num_gone_grating]), cad[num_gone], pre_contrast]
                print data
                #w.writerow(data)
                pygame.draw.rect(screen, background_colour, tx[(rightLeft+1)%2])

                time_elpased = round((second_time - initiate_time)/60, 2)
                if time_elpased >= 60:
                    print ("Time elapsed: " + str(time_elpased) + " minutes!")

                pygame.display.update()  # redraw background coclor
                print ("Punishment: " + "delay "+ str(punishment_time) + " second!")
                time.sleep(punishment_time) # time punishment

                # memory the choice
                fail_rechoice = 1
                
                break

        gone += 1
        if gone == 30:

            end_time = time.asctime( time.localtime(time.time()) )
            correct_ratio = float(correct_number) / gone
            #print ("The whole trial clear!")
            print ("Ending time: " + end_time )
            print ("It takes " + str(time_elpased) + " minutes to finish " + str(gone) + " trial!")
            print ("The ratio of correct: " + str(format(correct_ratio, '0.2%')))
            #w.writerow(["The ending time: ", end_time])
            #w.writerow(["It takes " + str(time_elpased) + " minutes to finish " + str(gone) + " trials!"])
            #w.writerow(["The ratio of correct: ", format(correct_ratio, '0.2%') ])

            break
    
    localtime = time.asctime( time.localtime(time.time()) )
    w.writerow([localtime]) # record the current time to the data
    w.writerow(["The ratio of correct in pre-test: ", format(correct_ratio, '0.2%'), "pre-contrast: ", pre_contrast ])
    data = ['tnum', 'correction', 'rt', 'rert', 'respos', 'corrpos', 'npix', 'a/c' , 'contrast']
    w.writerow(data)


    print ("Real test star!")
    initiate_time = time.time()
    localtime = time.asctime( time.localtime(time.time()) )
    print ("Starting time: " + localtime )
    
    
    # real test
    while True:
        
        # always start in center
        screen.blit(cue_img, (triWidth, 400))
        pygame.display.update()
        zero = time.time()


        while True:
            
            num_gone = re_gone % 10 # two kinds of sine wave negative of postitive
            num_gone_grating = re_gone % 1  # how many number it chose from the grating
            num_gone_contrast = re_gone % 24  # how many number it chose from the contrast
            #sen_gra = 'gabor_mix/gradient' + '4' + cad[num_gone] + '.png'
            sen_gra = 'gabor_mix/contrast' + str(num_contrast[num_gone_contrast]) + 'gradient' + str(blockd[num_gone_grating]) + cad[num_gone] + '.png'
            gra_img = pygame.image.load(sen_gra).convert()

            if  rc_time(pin_to_infra_mid) < sensi:
                # double check module
                if time.time() - zero < 0.5:
                    continue
                elif rc_time(pin_to_infra_mid) > sensi:
                    continue
                elif rc_time(pin_to_infra_mid) > sensi:
                    continue
                elif rc_time(pin_to_infra_mid) > sensi:
                    continue
                elif rc_time(pin_to_infra_mid) > sensi:
                    continue

                first_time = time.time()
                rightLeft = int(round(random.random()))
                pygame.draw.rect(screen, background_colour, tx[2])
                screen.blit(gra_img, ty[rightLeft])
                pygame.display.update()
                print(go[rightLeft])
                time.sleep(0.05)
                break
        
        """
        # broken module
        ev = pygame.event.get()
        for event in ev:
            peace = 1
        mk = 0
        while True:
            if mk:
                break
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.MOUSEBUTTONUP:
                    print "mouse click!"
                    first_time = time.time()
                    rightLeft = int(round(random.random()))
                    pygame.draw.rect(screen, background_colour, tx[2])
                    screen.blit(gra_img, ty[rightLeft])
                    pygame.display.update()
                    print(go[rightLeft])
                    mk = 1
        """
        while True:
            count1 = rc_time(cho[rightLeft])
            count2 = rc_time(cho[(rightLeft+1)%2])
            if count1 < sensi:
                # double check module
                if time.time()- first_time < 0.5:
                    continue
                elif rc_time(cho[rightLeft]) > sensi:
                    continue
                elif rc_time(cho[rightLeft]) > sensi:
                    continue
                elif rc_time(cho[rightLeft]) > sensi:
                    continue
                elif rc_time(cho[rightLeft]) > sensi:
                    continue

               
                
                second_time = time.time()

                # water module
                # uwater(wat[rightLeft])
                GPIO.output(wat[rightLeft], True)
                time.sleep(water_time)
                GPIO.output(wat[rightLeft], False)

                # data module
                print rightLeft, "Go center"
                data = [re_gone + 1, 1, second_time - first_time, first_time-zero, rightLeft, rightLeft, str(blockd[num_gone_grating]), cad[num_gone], num_contrast[num_gone_contrast]]
                print data
                w.writerow(data)
                pygame.draw.rect(screen, background_colour, tx[(rightLeft+1)%2])

                time_elpased = round((second_time - initiate_time)/60, 2)
                if time_elpased >= 60:
                    print ("Time elapsed: " + str(time_elpased) + " minutes!")

                break
            if count2 < sensi:
                # wrong choice, restart trial
                # double check module
                if time.time()- first_time < 0.5:
                    continue
                elif rc_time(cho[(rightLeft+1)%2]) > sensi:
                    continue
                elif rc_time(cho[(rightLeft+1)%2]) > sensi:
                    continue
                elif rc_time(cho[(rightLeft+1)%2]) > sensi:
                    continue
                elif rc_time(cho[(rightLeft+1)%2]) > sensi:
                    continue
                
                
                second_time= time.time()

                # sound module
                CS.play()
                time.sleep(0.2)
                CS.stop()

                # data module
                print rightLeft, " Wrong but go Center"
                data = [re_gone + 1, 0, second_time - first_time, first_time-zero, (not rightLeft)*1, rightLeft, str(blockd[num_gone_grating]), cad[num_gone], num_contrast[num_gone_contrast]]
                print data
                w.writerow(data)
                pygame.draw.rect(screen, background_colour, tx[(rightLeft+1)%2])

                time_elpased = round((second_time - initiate_time)/60, 2)
                if time_elpased >= 60:
                    print ("Time elapsed: " + str(time_elpased) + " minutes!")

                pygame.display.update()  # redraw background coclor
                
                print ("Punishment: " + "delay "+ str(punishment_time) + " second!")
                time.sleep(punishment_time) # time punishment
                
                break

        re_gone += 1
        if re_gone == 240:

            end_time = time.asctime( time.localtime(time.time()) )
            #correct_ratio = float(correct_number) / gone
            #print ("The whole trial clear!")
            print ("Ending time: " + end_time )
            print ("It takes " + str(time_elpased) + " minutes to finish " + str(re_gone) + " trial!")
            #print ("The ratio of correct: " + str(format(correct_ratio, '0.2%')))
            w.writerow(["The ending time: ", end_time])
            w.writerow(["It takes " + str(time_elpased) + " minutes to finish " + str(re_gone) + " trials!"])
           # w.writerow(["The ratio of correct: ", format(correct_ratio, '0.2%') ])

            break


except KeyboardInterrupt:

    end_time = time.asctime( time.localtime(time.time()) )
    second_time= time.time()
    time_elpased = round((second_time - initiate_time)/60, 2)
    print ("It takes " + str(time_elpased) + " minutes to finish " + str(re_gone) + " trial!")
    #correct_ratio = float(correct_number) / gone
    #print ("The ration of correct: " + str(format(correct_ratio, '0.2%')))
    w.writerow(["The ending time: ", end_time])
    w.writerow(["It takes " + str(time_elpased) + " minutes to finish " + str(re_gone) + " trials!"])
    #w.writerow(["The ratio of correct: ", format(correct_ratio, '0.2%' )])

    pass
finally:
    GPIO.cleanup()
    pygame.quit()
    f.close()
